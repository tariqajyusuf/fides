from typing import Union, Optional

from pydantic import BaseModel

from fides.api.models.connectionconfig import ConnectionType
from fides.api.schemas.connection_configuration.enums.system_type import SystemType


class ConnectionSystemTypeMap(BaseModel):
    """
    Describes the returned schema for connection types
    """

    identifier: Union[ConnectionType, str]
    type: SystemType
    human_readable: str
    encoded_icon: Optional[str]

    class Config:
        """Use enum values and set orm mode"""

        use_enum_values = True
        orm_mode = True
