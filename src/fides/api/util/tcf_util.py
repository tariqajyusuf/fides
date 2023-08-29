from functools import lru_cache
from typing import Callable, Dict, List, Optional, Set, Tuple, Type, Union

from fideslang.gvl import (
    GVL_FEATURES,
    GVL_SPECIAL_FEATURES,
    MAPPED_PURPOSES,
    MAPPED_SPECIAL_PURPOSES,
    data_use_to_purpose,
    feature_name_to_feature,
)
from fideslang.gvl.models import Feature, Purpose
from fideslang.models import LegalBasisForProcessingEnum
from sqlalchemy.engine import Row
from sqlalchemy.orm import Query, Session

from fides.api.models.privacy_preference import ConsentRecordType
from fides.api.models.sql_models import (  # type:ignore[attr-defined]
    PrivacyDeclaration,
    System,
)
from fides.api.schemas.tcf import (
    EmbeddedVendor,
    TCFFeatureRecord,
    TCFPurposeRecord,
    TCFVendorRecord,
)

# Each TCF section in the TCF Overlay mapped to the
# specific database field name from which previously-saved values are retrieved
TCF_COMPONENT_MAPPING: Dict[str, ConsentRecordType] = {
    "tcf_purposes": ConsentRecordType.purpose,
    "tcf_special_purposes": ConsentRecordType.special_purpose,
    "tcf_features": ConsentRecordType.feature,
    "tcf_special_features": ConsentRecordType.special_feature,
    "tcf_vendors": ConsentRecordType.vendor,
    "tcf_systems": ConsentRecordType.system,  # Systems where there are no known vendor id -
    # we don't know the system "type"
}


class TCFExperienceContents:
    """Class to serialize the initial contents of a TCF overlay

    Used to store GVL information pulled from Fideslang that has been combined with system data
    """

    tcf_purposes: List[TCFPurposeRecord] = []
    tcf_special_purposes: List[TCFPurposeRecord] = []
    tcf_vendors: List[TCFVendorRecord] = []
    tcf_features: List[TCFFeatureRecord] = []
    tcf_special_features: List[TCFFeatureRecord] = []
    tcf_systems: List[TCFVendorRecord] = []


def get_matching_privacy_declarations(
    db: Session, all_gvl_data_uses: List[str]
) -> Query:
    """Returns flattened system/privacy declaration records where we have a matching data gvl data use, and the
    legal basis for processing is consent or legitimate interest"""
    matching_privacy_declarations: Query = (
        db.query(
            System.id.label("system_id"),
            System.name.label("system_name"),
            System.description.label("system_description"),
            System.vendor_id,
            PrivacyDeclaration.data_use,
            PrivacyDeclaration.legal_basis_for_processing,
            PrivacyDeclaration.features,
        )
        .join(PrivacyDeclaration, System.id == PrivacyDeclaration.system_id)
        .filter(
            PrivacyDeclaration.data_use.in_(all_gvl_data_uses),
            PrivacyDeclaration.legal_basis_for_processing.in_(
                [
                    LegalBasisForProcessingEnum.CONSENT,
                    LegalBasisForProcessingEnum.LEGITIMATE_INTEREST,
                ]
            ),
        )
        .order_by(
            PrivacyDeclaration.created_at.desc()
        )  # Order to get repeatable results when collapsing information
    )
    return matching_privacy_declarations


def get_relevant_attributes_for_tcf_section(
    record: Row, relevant_uses_or_features: List[str], is_purpose_type: bool
) -> Set[str]:
    """
    Determine the set of relevant uses or features depending on the TCF section we're building
    """
    if is_purpose_type:
        return {record.data_use} if record.data_use in relevant_uses_or_features else {}

    unique_features = set()
    for feature_name in record.features:
        if feature_name in relevant_uses_or_features:
            unique_features.add(feature_name)
    return unique_features


def _get_tcf_functions_per_component_type(
    tcf_component_name: str,
) -> Tuple[Union[Type[TCFPurposeRecord], Type[TCFFeatureRecord]], Callable, bool]:
    """Helper for dynamically returning objects needed to build the TCF overlay
    depending on the type of TCF component"""

    is_purpose_type: bool = tcf_component_name in ["purposes", "special_purposes"]

    if is_purpose_type:
        return TCFPurposeRecord, data_use_to_purpose, is_purpose_type
    return TCFFeatureRecord, feature_name_to_feature, is_purpose_type


def build_tcf_section_and_update_system_map(
    relevant_uses_or_features: List[str],
    tcf_component_name: str,
    system_map: Dict[str, TCFVendorRecord],
    matching_privacy_declaration_query: Query,
) -> Tuple[
    Dict[int, Union[TCFPurposeRecord, TCFFeatureRecord]], Dict[str, TCFVendorRecord]
]:
    """Builds a [special ]purpose or [special ]feature section of the TCF Overlay as well as updates the systems section in place.

    Represents information in multiple formats.  Puts purposes and features at the top-level and embeds vendor and systems
    information underneath.  Likewise, puts vendor and system information top-level, and embeds purpose and feature information
    underneath.

    - System map is passed in as an argument instead of being constructed here, because both
    purposes/features are added to it and we modify that mapping multiple times.
    """
    (
        tcf_section_type,
        get_gvl_record,
        is_purpose_type,
    ) = _get_tcf_functions_per_component_type(
        tcf_component_name=tcf_component_name,
    )

    matching_purpose_or_feature_map: Dict[
        int, Union[TCFPurposeRecord, TCFFeatureRecord]
    ] = {}

    for privacy_declaration_row in matching_privacy_declaration_query:
        system_id: str = privacy_declaration_row["system_id"]
        vendor_id: Optional[str] = privacy_declaration_row["vendor_id"]
        system_identifier: str = vendor_id if vendor_id else system_id

        if system_identifier not in system_map:
            system_map[system_identifier] = TCFVendorRecord(
                id=system_identifier,  # Identify system by vendor id if it exists, otherwise use system id.
                # Collapses systems with same vendor id into one record.
                name=privacy_declaration_row.system_name,
                description=privacy_declaration_row.system_description,
                has_vendor_id=bool(
                    vendor_id
                ),  # Has_vendor_id will later let us separate into "tcf_vendors" and "tcf_systems"
            )

        # Pull the attributes we care about from the privacy declaration record
        # depending on the TCF section we're building.
        relevant_use_or_features: Set[str] = get_relevant_attributes_for_tcf_section(
            record=privacy_declaration_row,
            relevant_uses_or_features=relevant_uses_or_features,
            is_purpose_type=is_purpose_type,
        )

        for attribute in relevant_use_or_features:
            # Get the matching GVL record for the [special] purpose or [special] feature
            fideslang_gvl_record: Union[Purpose, Feature] = get_gvl_record(attribute)
            if not fideslang_gvl_record:
                continue

            # Transform the base gvl record into the TCF record type that has more elements for TCF display.
            # Will be a top-level section.
            tcf_record: Union[TCFPurposeRecord, TCFFeatureRecord] = tcf_section_type(
                **fideslang_gvl_record.dict()
            )
            # Clone the tcf_record before adding legal_bases. This will be a nested section beneath a system,
            # and will later contain only the legal bases that apply to that particular system, if applicable.
            embedded_tcf_record: Union[
                TCFPurposeRecord, TCFFeatureRecord
            ] = tcf_record.copy()

            # First, add the TCF record to the top-level section if it does not exist
            if tcf_record.id not in matching_purpose_or_feature_map:
                matching_purpose_or_feature_map[tcf_record.id] = tcf_record

            system_legal_bases = (
                [privacy_declaration_row.legal_basis_for_processing]
                if is_purpose_type
                and privacy_declaration_row.legal_basis_for_processing
                else []
            )

            # Update legal_bases in-place on the top-level record if applicable for purpose and special purpose sections
            extend_legal_bases(
                is_purpose_type,
                matching_purpose_or_feature_map[tcf_record.id],
                system_legal_bases,
            )

            # Now we embed a second-level TCF purpose/feature under the systems subsection
            system_subsection: List = getattr(
                system_map[system_identifier], tcf_component_name
            )

            existing_matching_record: Optional[
                TCFPurposeRecord, TCFFeatureRecord
            ] = next(
                (
                    tcf_sub_record
                    for tcf_sub_record in system_subsection
                    if tcf_sub_record.id == embedded_tcf_record.id
                ),  # Occurs when consolidating vendors
                None,
            )

            if existing_matching_record:
                # Update legal_bases on existing embedded TCF record beneath system
                extend_legal_bases(
                    is_purpose_type, existing_matching_record, system_legal_bases
                )
            else:
                # *Override* legal_bases for the cloned embedded purpose and special purpose record. Do not extend here
                # to ensure we just have legal_bases that apply for this particular system and purpose
                if is_purpose_type:
                    embedded_tcf_record.legal_bases = system_legal_bases
                # Embed new cloned TCF record beneath system
                system_subsection.append(embedded_tcf_record)

            # Finally, we do the reverse and embed the second-level system or vendor information
            # beneath the TCF purpose/feature section
            embedded_system_section: List[EmbeddedVendor] = (
                matching_purpose_or_feature_map[tcf_record.id].vendors
                if vendor_id
                else matching_purpose_or_feature_map[tcf_record.id].systems
            )
            if system_identifier not in [
                embedded_system_record.id
                for embedded_system_record in embedded_system_section
            ]:
                embedded_system_section.extend(
                    [
                        EmbeddedVendor(
                            id=system_identifier,
                            name=privacy_declaration_row.system_name,
                        )
                    ]
                )

            # Go ahead and sort embedded vendors by name while we're here.  Other sorting will occur at the end.
            embedded_system_section.sort(key=lambda x: x.name)

    return matching_purpose_or_feature_map, system_map


def extend_legal_bases(
    is_purpose_type: bool,
    purpose_record: TCFPurposeRecord,
    system_legal_bases: List[str],
):
    """Consolidates legal_bases in place if applicable"""
    if not is_purpose_type or not system_legal_bases:
        return

    purpose_record.legal_bases.extend(
        legal_basis
        for legal_basis in system_legal_bases
        if legal_basis not in purpose_record.legal_bases
    )
    purpose_record.legal_bases.sort()


@lru_cache()
def get_tcf_contents(
    db: Session,
) -> TCFExperienceContents:
    """
    Returns the base contents of the TCF overlay.

    Queries for systems/privacy declarations that have a relevant GVL data use and a legal basis of Consent or Legitimate interests,
    and builds the TCF Overlay from these systems and privacy declarations.

    TCF Overlay has Purpose, Special Purpose, Feature, and Special Feature Sections, that have relevant systems and vendors embedded underneath.
    The reverse representation is also returned, and Vendors and Systems each have relevant Purpose, Special Purpose, Feature, and Special Feature sections.
    """
    system_map: Dict[str, TCFVendorRecord] = {}

    all_tcf_data_uses: List[str] = []
    for purpose in MAPPED_PURPOSES.values():
        all_tcf_data_uses.extend(purpose.data_uses)

    special_purpose_data_uses: List[str] = []
    for special_purpose in MAPPED_SPECIAL_PURPOSES.values():
        special_purpose_data_uses.extend(special_purpose.data_uses)

    matching_privacy_declarations: Query = get_matching_privacy_declarations(
        db, all_tcf_data_uses + special_purpose_data_uses
    )

    # Collect purposes and update system map
    (
        purpose_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        all_tcf_data_uses,
        tcf_component_name="purposes",
        system_map=system_map,
        matching_privacy_declaration_query=matching_privacy_declarations,
    )

    # Collect special purposes and update system map
    (
        special_purpose_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        special_purpose_data_uses,
        tcf_component_name="special_purposes",
        system_map=updated_system_map,
        matching_privacy_declaration_query=matching_privacy_declarations,
    )

    # Collect features and update system map
    (
        feature_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        [feature.name for feature in GVL_FEATURES.values()],
        tcf_component_name="features",
        system_map=updated_system_map,
        matching_privacy_declaration_query=matching_privacy_declarations,
    )

    # Collect special features and update system map
    (
        special_feature_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        [feature.name for feature in GVL_SPECIAL_FEATURES.values()],
        tcf_component_name="special_features",
        system_map=updated_system_map,
        matching_privacy_declaration_query=matching_privacy_declarations,
    )

    return combine_overlay_sections(
        purpose_map,
        special_purpose_map,
        feature_map,
        special_feature_map,
        updated_system_map,
    )


def combine_overlay_sections(
    purpose_map: Dict[int, TCFPurposeRecord],
    special_purpose_map: Dict[int, TCFPurposeRecord],
    feature_map: Dict[int, TCFFeatureRecord],
    special_feature_map: Dict[int, TCFFeatureRecord],
    updated_system_map: Dict[str, TCFVendorRecord],
):
    """Combine the different TCF sections and sort purposes/features by id, and vendors by name"""
    tcf_consent_contents = TCFExperienceContents()
    tcf_consent_contents.tcf_purposes = _sort_by_id(purpose_map)
    tcf_consent_contents.tcf_special_purposes = _sort_by_id(special_purpose_map)
    tcf_consent_contents.tcf_features = _sort_by_id(feature_map)
    tcf_consent_contents.tcf_special_features = _sort_by_id(special_feature_map)

    sorted_vendors = _sort_by_name(updated_system_map)
    for vendor in sorted_vendors:
        vendor.purposes.sort(key=lambda x: x.id)
        vendor.special_purposes.sort(key=lambda x: x.id)
        vendor.features.sort(key=lambda x: x.id)
        vendor.special_features.sort(key=lambda x: x.id)

    tcf_consent_contents.tcf_vendors = []
    tcf_consent_contents.tcf_systems = []
    for system_or_vendor_record in sorted_vendors:
        if system_or_vendor_record.has_vendor_id:
            tcf_consent_contents.tcf_vendors.append(system_or_vendor_record)
        else:
            tcf_consent_contents.tcf_systems.append(system_or_vendor_record)

    return tcf_consent_contents


def _sort_by_id(
    tcf_mapping: Dict,
) -> List[Union[TCFPurposeRecord, TCFFeatureRecord, TCFVendorRecord]]:
    return sorted(list(tcf_mapping.values()), key=lambda x: x.id)


def _sort_by_name(
    tcf_mapping: Dict,
) -> List[Union[TCFPurposeRecord, TCFFeatureRecord, TCFVendorRecord]]:
    return sorted(list(tcf_mapping.values()), key=lambda x: x.name)
