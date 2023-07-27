from typing import Any, Dict, List, Optional

from fideslang.gvl import MAPPED_PURPOSES, MAPPED_SPECIAL_PURPOSES
from fideslang.gvl.models import MappedPurpose
from pydantic import root_validator, validator

from fides.api.models.privacy_notice import UserConsentPreference
from fides.api.schemas.base_class import FidesSchema
from fides.api.schemas.privacy_notice import UserSpecificConsentDetails


class TCFSavedandServedDetails(UserSpecificConsentDetails):
    """Default Schema that is supplements provided TCF details with whether a consent item was
    previously saved or served."""

    @root_validator
    def add_default_preference(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """For TCF purposes/special purposes, vendors, features, and special features,
        the default preferences are just 'opt-out'"""
        values["default_preference"] = UserConsentPreference.opt_out

        return values

    class Config:
        use_enum_values = True


class EmbeddedVendor(FidesSchema):
    """Sparse details for an embedded vendor.  Read-only."""

    id: str
    name: str


class TCFPurposeRecord(MappedPurpose, TCFSavedandServedDetails):
    """Schema for a TCF Purpose or a Special Purpose: returned in the TCF Overlay Experience"""

    vendors: List[EmbeddedVendor] = []  # Vendors that use this purpose


class EmbeddedLineItem(FidesSchema):
    """Sparse details for an embedded TCF line item within another TCF component. Read-only."""

    id: int
    name: str


class TCFDataCategoryRecord(FidesSchema):
    """Details for data categories on systems: Read-only"""

    id: str
    name: Optional[str]
    cookie: Optional[str]
    domain: Optional[str]
    duration: Optional[str]


class TCFVendorRecord(TCFSavedandServedDetails):
    """Schema for a TCF Vendor: returned in the TCF Overlay Experience"""

    id: str
    name: Optional[str]
    description: Optional[str]
    is_gvl: Optional[bool]
    purposes: List[EmbeddedLineItem] = []
    special_purposes: List[EmbeddedLineItem] = []
    data_categories: List[TCFDataCategoryRecord] = []
    features: List[EmbeddedLineItem] = []
    special_features: List[EmbeddedLineItem] = []


class TCFFeatureRecord(TCFSavedandServedDetails):
    """Schema for a TCF Feature or a special feature: returned in the TCF Overlay Experience
    TODO: TCF Flesh out TCFFeatureRecord
    """

    id: int
    name: Optional[str]


class TCFPreferenceSaveBase(FidesSchema):
    """Base schema for saving individual TCF component preferences"""

    id: int
    preference: UserConsentPreference
    served_notice_history_id: Optional[str]


class TCFPurposeSave(TCFPreferenceSaveBase):
    """Schema for saving preferences with respect to a TCF Purpose"""

    @validator("id")
    @classmethod
    def validate_purpose_id(cls, value: int) -> int:
        """
        Validate purpose id is valid
        """
        if value not in MAPPED_PURPOSES:
            raise ValueError(
                f"Cannot save preferences against invalid purpose id: '{value}'"
            )
        return value


class TCFSpecialPurposeSave(TCFPreferenceSaveBase):
    """Schema for saving preferences with respect to a TCF Special Purpose"""

    @validator("id")
    @classmethod
    def validate_special_purpose_id(cls, value: int) -> int:
        """
        Validate special purpose id is valid
        """
        if value not in MAPPED_SPECIAL_PURPOSES:
            raise ValueError(
                f"Cannot save preferences against invalid special purpose id: '{value}'"
            )
        return value


class TCFVendorSave(FidesSchema):
    """Base schema for saving preferences with respect to a TCF Vendor
    TODO: TCF Add validation for allowable features
    """

    id: str
    preference: UserConsentPreference
    served_notice_history_id: Optional[str]


class TCFFeatureSave(TCFPreferenceSaveBase):
    """Schema for saving a user's preference with respect to a TCF feature
    TODO: TCF Add validation for allowable features
    """


class TCFSpecialFeatureSave(TCFPreferenceSaveBase):
    """Schema for saving a user's preference with respect to a TCF special feature
    TODO: TCF Add validation for allowable special features
    """
