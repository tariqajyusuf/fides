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
from sqlalchemy import case, func
from sqlalchemy.dialects.postgresql import array, array_agg
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
    """Schema to serialize the initial contents of a TCF overlay

    Used to store GVL information pulled from Fideslang that has been combined with system data
    """

    tcf_purposes: List[TCFPurposeRecord] = []
    tcf_special_purposes: List[TCFPurposeRecord] = []
    tcf_vendors: List[TCFVendorRecord] = []
    tcf_features: List[TCFFeatureRecord] = []
    tcf_special_features: List[TCFFeatureRecord] = []
    tcf_systems: List[TCFVendorRecord] = []


def get_system_features(record: Row, relevant_features: List[str]) -> Set[str]:
    """Collapses the relevant features across all the privacy declarations on the current system into a set.
    Sometimes the relevant features might be "TCF Features" - other times they might be "TCF Special Features"
    """
    unique_features = set()
    for feature_list in record.features:
        for feature_name in feature_list:
            if feature_name in relevant_features:
                unique_features.add(feature_name)
    return unique_features


def _get_tcf_functions_per_component_type(
    db: Session,
    tcf_component_name: str,
    relevant_uses_or_features: List[str],
) -> Tuple[
    Query, Union[Type[TCFPurposeRecord], Type[TCFFeatureRecord]], Callable, bool
]:
    """Helper for dynamically returning objects needed to build the TCF overlay
    depending on the type of TCF component"""
    tcf_record_type: Union[Type[TCFPurposeRecord], Type[TCFFeatureRecord]]
    get_gvl_construct: Callable
    is_purpose_type: bool = tcf_component_name in ["purposes", "special_purposes"]

    matching_systems: Query = (
        db.query(
            System.id,
            System.name,
            System.description,
            System.vendor_id,
            array_agg(
                array(
                    [
                        PrivacyDeclaration.data_use,
                        PrivacyDeclaration.legal_basis_for_processing,
                    ]
                )
            ).label(
                "data_use_and_legal_bases_list_of_lists"
            ),  # A list of lists with a data use and a legal basis for each privacy declaration
            array_agg(
                case(
                    [
                        (
                            func.array_length(PrivacyDeclaration.features, 1) > 0,
                            PrivacyDeclaration.features,
                        )
                    ],
                    else_=[
                        "skip"
                    ],  # Default since you can't use array_agg on empty arrays.  ["skip"] is filtered out later.
                )
            ).label("features"),
        )
        .join(PrivacyDeclaration, System.id == PrivacyDeclaration.system_id)
        .group_by(System.id)
        .order_by(
            System.created_at.desc()
        )  # Order by to get repeatable results when collapsing information
    )

    if is_purpose_type:
        matching_systems = matching_systems.filter(
            PrivacyDeclaration.data_use.in_(relevant_uses_or_features)
        )
        tcf_record_type = TCFPurposeRecord
        get_gvl_construct = data_use_to_purpose
    else:
        matching_systems = matching_systems.filter(
            PrivacyDeclaration.features.overlap(relevant_uses_or_features)
        )
        tcf_record_type = TCFFeatureRecord
        get_gvl_construct = feature_name_to_feature

    return (
        matching_systems,
        tcf_record_type,
        get_gvl_construct,
        is_purpose_type,
    )


def build_tcf_section_and_update_system_map(
    db: Session,
    relevant_uses_or_features: List[str],
    tcf_component_name: str,
    system_map: Dict[str, TCFVendorRecord],
) -> Tuple[
    Dict[int, Union[TCFPurposeRecord, TCFFeatureRecord]], Dict[str, TCFVendorRecord]
]:
    """Helper method for building data for a specific portion of the TCF overlay, depending on the tcf_component_name.

    Represents information in multiple formats.  Puts purposes and features at the top-level and embeds vendor and systems
    information underneath.  Likewise, puts vendor and system information top-level, and embeds purpose and feature information
    underneath.

    - System map is passed in as an argument instead of being constructed here, because both
    purposes/features are added to it and we modify that mapping multiple times.
    """
    (
        matching_systems,
        tcf_section_type,
        get_gvl_record,
        is_purpose_type,
    ) = _get_tcf_functions_per_component_type(
        db=db,
        tcf_component_name=tcf_component_name,
        relevant_uses_or_features=relevant_uses_or_features,
    )

    matching_purpose_or_feature_map: Dict[
        int, Union[TCFPurposeRecord, TCFFeatureRecord]
    ] = {}

    for system in matching_systems:
        system_id: str = system["id"]
        vendor_id: Optional[str] = system["vendor_id"]
        system_identifier: str = vendor_id if vendor_id else system_id

        if system_identifier not in system_map:
            system_map[system_identifier] = TCFVendorRecord(
                id=system_identifier,  # Identify system by vendor id if it exists, otherwise use system id.
                # Collapses systems with same vendor id into one record.
                name=system.name,
                description=system.description,
                has_vendor_id=bool(
                    vendor_id
                ),  # Has_vendor_id will later let us separate into "tcf_vendors" and "tcf_systems"
            )

        # Pull the attributes we care about from the system record depending on the TCF section we're building.
        relevant_system_attributes: Set[str] = (
            [data_use[0] for data_use in system.data_use_and_legal_bases_list_of_lists]
            if is_purpose_type
            else get_system_features(
                system, relevant_features=relevant_uses_or_features
            )
        )

        for item in relevant_system_attributes:
            # Get the matching GVL record for the [special] purpose or [special] feature
            fideslang_gvl_record: Union[Purpose, Feature] = get_gvl_record(item)
            if not fideslang_gvl_record:
                continue

            # Transform the base gvl record into the TCF record type that has more elements for TCF display.
            # Will be a top-level section.
            tcf_record: Union[TCFPurposeRecord, TCFFeatureRecord] = tcf_section_type(
                **fideslang_gvl_record.dict()
            )
            # Clone the tcf_record. This will be a nested section beneath a system, and will contain only the
            # legal bases that apply to that system, if applicable.
            embedded_tcf_record: Union[
                TCFPurposeRecord, TCFFeatureRecord
            ] = tcf_record.copy()

            # First, add the top-level TCF record if it does not exist
            if tcf_record.id not in matching_purpose_or_feature_map:
                matching_purpose_or_feature_map[tcf_record.id] = tcf_record

            # Consolidate a list of legal_bases across relevant privacy declarations
            system_legal_bases = (
                list(
                    {
                        use_legal_basis_pair[1]
                        for use_legal_basis_pair in system.data_use_and_legal_bases_list_of_lists
                        if use_legal_basis_pair[1]
                        and use_legal_basis_pair[0] in tcf_record.data_uses
                    }
                )
                if is_purpose_type
                else []
            )

            # Update legal_bases in-place in the top-level record if applicable for purpose and special purpose sections
            extend_legal_bases(
                is_purpose_type,
                matching_purpose_or_feature_map[tcf_record.id],
                system_legal_bases,
            )

            # Now we embed the second-level TCF purpose/feature under the systems subsection
            system_subsection = getattr(
                system_map[system_identifier], tcf_component_name
            )

            existing_matching_record = next(
                (
                    tcf_sub_record
                    for tcf_sub_record in system_subsection
                    if tcf_sub_record.id == tcf_record.id
                ),  # Occurs when consolidating vendors
                None,
            )

            if existing_matching_record:
                # Update legal_bases on embedded tcf record beneath system
                extend_legal_bases(
                    is_purpose_type, existing_matching_record, system_legal_bases
                )
            else:
                # *Override* legal_bases for embedded purpose and special purpose record. Do not extend because embedded
                # purpose records should only have the legal_bases that apply to this particular system.
                if is_purpose_type:
                    embedded_tcf_record.legal_bases = system_legal_bases
                # Embed tcf record beneath system
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
                    [EmbeddedVendor(id=system_identifier, name=system.name)]
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

    Loads TCF Purposes and Special Purposes from Fideslang and then returns a subset of those whose data uses
    are on systems.

    Similarly returns Features and Special Features from fideslang that are on the systems.

    Returns a reverse representation for the vendors and systems themselves.
    """
    system_map: Dict[str, TCFVendorRecord] = {}

    # Collect purposes and update system map
    all_tcf_data_uses: List[str] = []
    for purpose in MAPPED_PURPOSES.values():
        all_tcf_data_uses.extend(purpose.data_uses)
    (
        purpose_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        db, all_tcf_data_uses, tcf_component_name="purposes", system_map=system_map
    )

    # Collect special purposes and update system map
    special_purpose_data_uses: List[str] = []
    for special_purpose in MAPPED_SPECIAL_PURPOSES.values():
        special_purpose_data_uses.extend(special_purpose.data_uses)
    (
        special_purpose_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        db,
        special_purpose_data_uses,
        tcf_component_name="special_purposes",
        system_map=updated_system_map,
    )

    # Collect features and update system map
    (
        feature_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        db,
        [feature.name for feature in GVL_FEATURES.values()],
        tcf_component_name="features",
        system_map=updated_system_map,
    )

    # Collect special features and update system map
    (
        special_feature_map,
        updated_system_map,
    ) = build_tcf_section_and_update_system_map(
        db,
        [feature.name for feature in GVL_SPECIAL_FEATURES.values()],
        tcf_component_name="special_features",
        system_map=updated_system_map,
    )

    # Sort purposes/features by id, and vendors by name
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
