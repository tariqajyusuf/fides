from sqlalchemy import Column, String

from fides.lib.db.base_class import Base


class CustomConnectorTemplate(Base):
    """A model representing a custom connector template"""

    key = Column(String, index=True, unique=True, nullable=False)
    name = Column(String, index=False, unique=False, nullable=False)
    config = Column(String, index=False, unique=False, nullable=False)
    dataset = Column(String, index=False, unique=False, nullable=False)
    icon = Column(String, index=False, unique=False, nullable=True)
    functions = Column(String, index=False, unique=False, nullable=True)
