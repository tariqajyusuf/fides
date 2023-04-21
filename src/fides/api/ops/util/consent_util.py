from typing import List, Optional, Type, Union

import yaml
from loguru import logger
from sqlalchemy.orm import Session

from fides.api.ctl.sql_models import DataUse, System  # type: ignore[attr-defined]
from fides.api.custom_types import SafeStr
from fides.api.ops.models.privacy_notice import (
    EnforcementLevel,
    PrivacyNotice,
    PrivacyNoticeTemplate,
    check_conflicting_data_uses,
)
from fides.api.ops.models.privacy_preference import (
    PrivacyPreferenceHistory,
    UserConsentPreference,
)
from fides.api.ops.models.privacy_request import PrivacyRequest
from fides.api.ops.schemas.privacy_notice import PrivacyNoticeCreation


def filter_privacy_preferences_for_propagation(
    system: Optional[System], privacy_preferences: List[PrivacyPreferenceHistory]
) -> List[PrivacyPreferenceHistory]:
    """Filter privacy preferences on a privacy request to just the ones that should be considered for third party
    consent propagation"""

    propagatable_preferences: List[PrivacyPreferenceHistory] = [
        pref
        for pref in privacy_preferences
        if pref.privacy_notice_history.enforcement_level == EnforcementLevel.system_wide
        and pref.preference != UserConsentPreference.acknowledge
    ]

    if not system:
        return propagatable_preferences

    filtered_on_use: List[PrivacyPreferenceHistory] = []
    for pref in propagatable_preferences:
        if pref.privacy_notice_history.applies_to_system(system):
            filtered_on_use.append(pref)
    return filtered_on_use


def should_opt_in_to_service(
    system: Optional[System], privacy_request: PrivacyRequest
) -> Optional[bool]:
    """
    Determine if we should opt in (return True), opt out (return False), or do nothing (return None) for the given System.

    - If using the old workflow (privacyrequest.consent_preferences), return True if all attached consent preferences
    are opt in, otherwise False.  System check is ignored.

    - If using the new workflow (privacyrequest.privacy_preferences), there is more filtering here.  Privacy Preferences
    must have an enforcement level of system-wide and a data use must match a system data use.  If the connector is
    orphaned (no system), skip the data use check. If conflicts, prefer the opt-out preference.
    """

    # OLD WORKFLOW
    if privacy_request.consent_preferences:
        return all(
            consent_pref["opt_in"]
            for consent_pref in privacy_request.consent_preferences
        )

    # NEW WORKFLOW
    filtered_preferences = filter_privacy_preferences_for_propagation(
        system, privacy_request.privacy_preferences
    )
    if not filtered_preferences:
        return None  # We should do nothing here

    return all(
        filtered_pref.preference == UserConsentPreference.opt_in
        for filtered_pref in filtered_preferences
    )


def validate_notice_data_uses(
    privacy_notices: List[PrivacyNoticeCreation],
    db: Session,
) -> None:
    """
    Ensures that all the provided `PrivacyNotice`s have valid data uses.
    """
    valid_data_uses = [data_use.fides_key for data_use in DataUse.query(db).all()]
    for privacy_notice in privacy_notices:
        privacy_notice.validate_data_uses(valid_data_uses)


def create_privacy_notices_util(
    db: Session,
    privacy_notice_schemas: List[PrivacyNoticeCreation],
    model: Union[Type[PrivacyNotice], Type[PrivacyNoticeTemplate]],
) -> List[Union[PrivacyNotice, PrivacyNoticeTemplate]]:
    """Reusable method to validate and create a PrivacyNotice or a PrivacyNoticeTemplate.

    Creating a PrivacyNotice also has a side effect of creating a historical record in PrivacyNoticeHistory
    """
    validate_notice_data_uses(privacy_notice_schemas, db)

    existing_notices = model.query(db).filter(model.disabled.is_(False)).all()  # type: ignore[attr-defined]

    new_notices = [
        model(**privacy_notice.dict(exclude_unset=True))
        for privacy_notice in privacy_notice_schemas
    ]
    check_conflicting_data_uses(new_notices, existing_notices)

    return [
        model.create(
            db=db, data=privacy_notice.dict(exclude_unset=True), check_name=False
        )
        for privacy_notice in privacy_notice_schemas
    ]


def load_default_notices(
    db: Session, notice_yaml_file_path: str
) -> List[PrivacyNotice]:
    """Populates default PrivacyNoticeTemplates, and then loads these templates into the
    PrivacyNoticeHistory and PrivacyNotice tables, making them available for use.
    """
    logger.info("Loading default notices from {}", notice_yaml_file_path)
    with open(notice_yaml_file_path, "r", encoding="utf-8") as file:
        notices = yaml.safe_load(file).get("privacy_notices", [])

        template_schemas: List[PrivacyNoticeCreation] = []

        # Validate templates
        for privacy_notice_data in notices:
            template_schemas.append(PrivacyNoticeCreation(**privacy_notice_data))

        # Create Privacy Notice Templates
        privacy_notice_templates: List[
            PrivacyNoticeTemplate
        ] = create_privacy_notices_util(
            db, template_schemas, PrivacyNoticeTemplate
        )  # type: ignore[assignment]

        # Link Privacy Notice Schemas to the Privacy Notice Templates
        notice_schemas: List[PrivacyNoticeCreation] = []
        for template in privacy_notice_templates:
            privacy_notice_schema = PrivacyNoticeCreation.from_orm(template)
            privacy_notice_schema.origin = SafeStr(template.id)
            notice_schemas.append(privacy_notice_schema)

        # Create PrivacyNotice and PrivacyNoticeHistory records
        privacy_notices: List[PrivacyNotice] = create_privacy_notices_util(  # type: ignore[assignment]
            db, notice_schemas, PrivacyNotice
        )

        return privacy_notices
