from typing import List, Optional

from pydantic import Field

from fides.api.schemas.base_class import NoValidationSchema
from fides.api.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class PostgreSQLSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a PostgreSQL Database"""

    host: str = Field(
        title="Host",
        description="The hostname or IP address of the server where the database is running.",
    )
    port: int = Field(
        5432,
        title="Port",
        description="The network port number on which the server is listening for incoming connections (default: 5432).",
    )
    username: str = Field(
        title="Username",
        description="The user account used to authenticate and access the database.",
    )
    password: str = Field(
        title="Password",
        description="The password used to authenticate and access the database.",
        sensitive=True,
    )
    dbname: str = Field(
        title="Database",
        description="The name of the specific database within the database server that you want to connect to.",
    )
    db_schema: str = Field(
        "public",
        title="Schema",
        description="The default schema to be used for the database connection (defaults to public).",
    )
    ssh_required: bool = Field(
        False,
        title="SSH Required",
        description="Indicates whether an SSH tunnel is required for the connection. Enable this option if your PostgreSQL server is behind a firewall and requires SSH tunneling for remote connections.",
    )

    _required_components: List[str] = [
        "host",
        "port",
        "username",
        "password",
        "dbname",
        "db_schema",
        "ssh_required",
    ]


class PostgreSQLDocsSchema(PostgreSQLSchema, NoValidationSchema):
    """Postgres Secrets Schema for API Docs"""
