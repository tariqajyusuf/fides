from uuid import uuid4

import pytest

from fides.api.models.sql_models import PrivacyDeclaration
from fides.api.models.tcf_publisher_overrides import TCFPublisherOverrides
from fides.api.util.tcf.tcf_experience_contents import get_matching_privacy_declarations


class TestPrivacyDeclarationInstanceLevelHybridProperties:
    """Test some instance-level hybrid properties defined on the Privacy Declaration
    related to Publisher Overrides"""

    def test_privacy_declaration_enable_override_is_false(self, system, db):
        """Enable override is false so overridden legal basis is going to default
        to the defined legal basis"""
        pd = PrivacyDeclaration(
            name=f"declaration-name-{uuid4()}",
            data_categories=[],
            data_use="analytics.reporting.campaign_insights",
            data_subjects=[],
            data_qualifier="aggregated_data",
            dataset_references=[],
            ingress=None,
            egress=None,
            legal_basis_for_processing="Consent",
            system_id=system.id,
        ).save(db=db)

        assert pd.purpose == 9
        assert pd._publisher_override_legal_basis_join is None
        assert pd._publisher_override_is_included_join is None
        assert pd.overridden_legal_basis_for_processing == "Consent"

    @pytest.mark.usefixtures(
        "enable_override_vendor_purposes",
    )
    def test_enable_override_is_true_but_no_matching_purpose(self, system, db):
        """Privacy Declaration has Special Purpose not Purpose, so no overrides applicable"""
        pd = PrivacyDeclaration(
            name=f"declaration-name-{uuid4()}",
            data_categories=[],
            data_use="essential.fraud_detection",
            data_subjects=[],
            data_qualifier="aggregated_data",
            dataset_references=[],
            ingress=None,
            egress=None,
            legal_basis_for_processing="Consent",
            system_id=system.id,
        ).save(db)

        assert pd.purpose is None
        assert pd._publisher_override_legal_basis_join is None
        assert pd._publisher_override_is_included_join is None
        assert pd.overridden_legal_basis_for_processing == "Consent"

    @pytest.mark.usefixtures(
        "enable_override_vendor_purposes",
    )
    def test_enable_override_is_true_but_purpose_is_excluded(self, db, system):
        """Purpose is overridden as excluded, so legal basis returns as None, to match
        class-wide override"""
        TCFPublisherOverrides.create(
            db,
            data={
                "purpose": 9,
                "is_included": False,
            },
        )

        pd = PrivacyDeclaration(
            name="declaration-name",
            data_categories=[],
            data_use="analytics.reporting.campaign_insights",
            data_subjects=[],
            data_qualifier="aggregated_data",
            dataset_references=[],
            ingress=None,
            egress=None,
            flexible_legal_basis_for_processing=True,
            legal_basis_for_processing="Consent",
            system_id=system.id,
        ).save(db=db)

        assert pd.purpose == 9
        assert pd._publisher_override_legal_basis_join is None
        assert pd._publisher_override_is_included_join is False
        assert pd.overridden_legal_basis_for_processing is None

    @pytest.mark.usefixtures(
        "enable_override_vendor_purposes",
    )
    def test_publisher_override_defined_but_no_required_legal_basis_specified(
        self, db, system
    ):
        """Purpose override is defined, but no legal basis override"""
        TCFPublisherOverrides.create(
            db,
            data={
                "purpose": 9,
                "is_included": True,
            },
        )

        pd = PrivacyDeclaration(
            name="declaration-name",
            data_categories=[],
            data_use="analytics.reporting.campaign_insights",
            data_subjects=[],
            data_qualifier="aggregated_data",
            dataset_references=[],
            ingress=None,
            egress=None,
            flexible_legal_basis_for_processing=True,
            legal_basis_for_processing="Consent",
            system_id=system.id,
        ).save(db=db)

        assert pd.purpose == 9
        assert pd._publisher_override_legal_basis_join is None
        assert pd._publisher_override_is_included_join is True
        assert pd.overridden_legal_basis_for_processing == "Consent"

    @pytest.mark.usefixtures(
        "enable_override_vendor_purposes",
    )
    def test_publisher_override_defined_with_required_legal_basis_specified(
        self, db, system
    ):
        """Purpose override is defined, but no legal basis override"""
        TCFPublisherOverrides.create(
            db,
            data={
                "purpose": 9,
                "is_included": True,
                "required_legal_basis": "Legitimate interests",
            },
        )

        pd = PrivacyDeclaration(
            name="declaration-name",
            data_categories=[],
            data_use="analytics.reporting.campaign_insights",
            data_subjects=[],
            data_qualifier="aggregated_data",
            dataset_references=[],
            ingress=None,
            egress=None,
            flexible_legal_basis_for_processing=True,
            legal_basis_for_processing="Consent",
            system_id=system.id,
        ).save(db=db)

        assert pd.purpose == 9
        assert pd._publisher_override_legal_basis_join == "Legitimate interests"
        assert pd._publisher_override_is_included_join is True
        assert pd.overridden_legal_basis_for_processing == "Legitimate interests"


class TestMatchingPrivacyDeclarations:
    """Tests matching privacy declarations returned that are the basis of the TCF Experience and the "relevant_systems"
    that are saved for consent reporting
    """

    @pytest.mark.usefixtures(
        "emerse_system",
    )
    def test_get_matching_privacy_declarations_enable_purpose_override_is_false(
        self, emerse_system, db
    ):
        declarations = get_matching_privacy_declarations(db)

        assert declarations.count() == 13

        mapping = {
            declaration.data_use: declaration.purpose for declaration in declarations
        }

        # marketing.advertising.serving, essential.service.security, essential.fraud_detection map to special purposes, not purposes
        assert mapping == {
            "marketing.advertising.serving": None,
            "essential.service.security": None,
            "essential.fraud_detection": None,
            "analytics.reporting.campaign_insights": 9,
            "analytics.reporting.content_performance": 8,
            "analytics.reporting.ad_performance": 7,
            "marketing.advertising.frequency_capping": 2,
            "marketing.advertising.first_party.contextual": 2,
            "marketing.advertising.negative_targeting": 2,
            "marketing.advertising.first_party.targeted": 4,
            "marketing.advertising.third_party.targeted": 4,
            "marketing.advertising.profiling": 3,
            "functional.storage": 1,
        }

    @pytest.mark.usefixtures("emerse_system", "enable_override_vendor_purposes")
    def test_privacy_declaration_publisher_overrides(
        self,
        db,
    ):
        """Define some purpose legal basis overrides and check their effects on what is returned in the Privacy Declaration query"""

        # Defined legal basis is also Consent for purpose 1 on Emerse.
        # Publisher override matches.
        TCFPublisherOverrides.create(
            db,
            data={"purpose": 1, "is_included": True, "required_legal_basis": "Consent"},
        )

        # Defined legal basis is Legitimate Interests for purpose 2 on Emerse.
        # Here, Purpose 2 is specified to be excluded.
        TCFPublisherOverrides.create(
            db,
            data={
                "purpose": 2,
                "is_included": False,
            },
        )

        # Defined legal basis is Consent for purpose 3 on Emerse.
        # No legal basis override is defined.
        TCFPublisherOverrides.create(
            db,
            data={
                "purpose": 3,
                "is_included": True,
                "required_legal_basis": None,
            },
        )

        # Defined legal basis is Consent for purpose 4 on Emerse.
        # Override here has a different legal basis
        TCFPublisherOverrides.create(
            db,
            data={
                "purpose": 4,
                "is_included": True,
                "required_legal_basis": "Legitimate interests",
            },
        )

        declarations = get_matching_privacy_declarations(db)

        legal_basis_overrides = {
            declaration.purpose: declaration.legal_basis_for_processing
            for declaration in declarations
            if declaration.purpose
        }

        # Purpose 2 has been removed altogether and Purpose 4 Legal Basis
        # has been overridden to Legitimate Interests legal basis
        assert legal_basis_overrides == {
            9: "Legitimate interests",
            8: "Legitimate interests",
            7: "Legitimate interests",
            4: "Legitimate interests",
            3: "Consent",
            1: "Consent",
        }

        original_legal_basis = {
            declaration.purpose: declaration.original_legal_basis_for_processing
            for declaration in declarations
            if declaration.purpose
        }
        assert original_legal_basis == {
            9: "Legitimate interests",
            8: "Legitimate interests",
            7: "Legitimate interests",
            4: "Consent",
            3: "Consent",
            1: "Consent",
        }

        # The three declarations on Emerse with data uses mapping to Purpose 2 have been excluded
        assert declarations.count() == 10
