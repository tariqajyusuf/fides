import io
import zipfile
from io import BytesIO
from typing import Any, Dict, Optional
from zipfile import BadZipFile, ZipFile

from fastapi import Depends, File, HTTPException, UploadFile
from fastapi.params import Security
from loguru import logger
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from fides.api.ops.api import deps
from fides.api.ops.api.v1.endpoints.connection_endpoints import validate_secrets
from fides.api.ops.api.v1.scope_registry import (
    CONNECTION_AUTHORIZE,
    CONNECTOR_TEMPLATE_REGISTER,
    SAAS_CONFIG_CREATE_OR_UPDATE,
    SAAS_CONFIG_DELETE,
    SAAS_CONFIG_READ,
    SAAS_CONNECTION_INSTANTIATE,
)
from fides.api.ops.api.v1.urn_registry import (
    AUTHORIZE,
    CONNECTION_TYPES,
    REGISTER_CONNECTOR_TEMPLATE,
    SAAS_CONFIG,
    SAAS_CONFIG_VALIDATE,
    SAAS_CONNECTOR_FROM_TEMPLATE,
    V1_URL_PREFIX,
)
from fides.api.ops.common_exceptions import FidesopsException
from fides.api.ops.models.connectionconfig import ConnectionConfig, ConnectionType
from fides.api.ops.models.custom_connector_template import CustomConnectorTemplate
from fides.api.ops.models.datasetconfig import DatasetConfig
from fides.api.ops.schemas.connection_configuration.connection_config import (
    SaasConnectionTemplateResponse,
    SaasConnectionTemplateValues,
)
from fides.api.ops.schemas.dataset import FidesopsDataset
from fides.api.ops.schemas.saas.saas_config import (
    SaaSConfig,
    SaaSConfigValidationDetails,
    ValidateSaaSConfigResponse,
)
from fides.api.ops.schemas.shared_schemas import FidesOpsKey
from fides.api.ops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fides.api.ops.service.authentication.authentication_strategy_oauth2_authorization_code import (
    OAuth2AuthorizationCodeAuthenticationStrategy,
)
from fides.api.ops.service.connectors.saas.connector_registry_service import (
    ConnectorRegistry,
    ConnectorTemplate,
    create_connection_config_from_template_no_save,
    load_registry,
    register_custom_functions,
    upsert_dataset_config_from_template,
)
from fides.api.ops.util.api_router import APIRouter
from fides.api.ops.util.oauth_util import verify_oauth_client
from fides.api.ops.util.saas_util import (
    load_config_from_string,
    load_dataset_from_string,
)
from fides.lib.exceptions import KeyOrNameAlreadyExists

router = APIRouter(tags=["SaaS Configs"], prefix=V1_URL_PREFIX)

# Helper method to inject the parent ConnectionConfig into these child routes
def _get_saas_connection_config(
    connection_key: FidesOpsKey, db: Session = Depends(deps.get_db)
) -> ConnectionConfig:
    logger.info("Finding connection config with key '{}'", connection_key)
    connection_config = ConnectionConfig.get_by(db, field="key", value=connection_key)
    if not connection_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No connection config with key '{connection_key}'",
        )
    if connection_config.connection_type != ConnectionType.saas:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="This action is only applicable to connection configs of connection type 'saas'",
        )
    return connection_config


def verify_oauth_connection_config(
    connection_config: Optional[ConnectionConfig],
) -> None:
    """
    Verifies that the connection config is present and contains
    the necessary configurations for OAuth2 Authorization Code authentication.
    Returns an HTTPException with the appropriate error message indicating
    which configurations are missing or incorrect.
    """

    if not connection_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The connection config cannot be found.",
        )

    saas_config = connection_config.get_saas_config()
    if not saas_config:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The connection config does not contain a SaaS config.",
        )

    authentication = saas_config.client_config.authentication
    if not authentication:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The connection config does not contain an authentication configuration.",
        )

    if authentication.strategy != OAuth2AuthorizationCodeAuthenticationStrategy.name:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The connection config does not use OAuth2 Authorization Code authentication.",
        )


@router.put(
    SAAS_CONFIG_VALIDATE,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_READ])],
    status_code=HTTP_200_OK,
    response_model=ValidateSaaSConfigResponse,
)
def validate_saas_config(
    saas_config: SaaSConfig,
) -> ValidateSaaSConfigResponse:
    """
    Uses the SaaSConfig Pydantic model to validate the SaaS config
    without attempting to save it to the database.

    Checks that:
    - all required fields are present, all field values are valid types
    - each connector_param only has one of references or identity, not both
    """

    logger.info("Validation successful for SaaS config '{}'", saas_config.fides_key)
    return ValidateSaaSConfigResponse(
        saas_config=saas_config,
        validation_details=SaaSConfigValidationDetails(
            msg="Validation successful",
        ),
    )


@router.patch(
    SAAS_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_CREATE_OR_UPDATE])],
    status_code=HTTP_200_OK,
    response_model=SaaSConfig,
)
def patch_saas_config(
    saas_config: SaaSConfig,
    db: Session = Depends(deps.get_db),
    connection_config: ConnectionConfig = Depends(_get_saas_connection_config),
) -> SaaSConfig:
    """
    Given a SaaS config element, update the corresponding ConnectionConfig object
    or report failure
    """
    logger.info(
        "Updating SaaS config '{}' on connection config '{}'",
        saas_config.fides_key,
        connection_config.key,
    )
    connection_config.update_saas_config(db, saas_config=saas_config)
    return connection_config.saas_config  # type: ignore


@router.get(
    SAAS_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_READ])],
    response_model=SaaSConfig,
)
def get_saas_config(
    connection_config: ConnectionConfig = Depends(_get_saas_connection_config),
) -> SaaSConfig:
    """Returns the SaaS config for the given connection config."""

    logger.info("Finding SaaS config for connection '{}'", connection_config.key)
    saas_config = connection_config.saas_config
    if not saas_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No SaaS config found for connection '{connection_config.key}'",
        )
    return saas_config


@router.delete(
    SAAS_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONFIG_DELETE])],
    status_code=HTTP_204_NO_CONTENT,
)
def delete_saas_config(
    db: Session = Depends(deps.get_db),
    connection_config: ConnectionConfig = Depends(_get_saas_connection_config),
) -> None:
    """Removes the SaaS config for the given connection config.
    The corresponding dataset and secrets must be deleted before deleting the SaaS config"""

    logger.info("Finding SaaS config for connection '{}'", connection_config.key)
    saas_config = connection_config.saas_config
    if not saas_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No SaaS config found for connection '{connection_config.key}'",
        )

    fides_key = saas_config.get("fides_key")
    dataset = DatasetConfig.filter(
        db=db,
        conditions=(
            (DatasetConfig.connection_config_id == connection_config.id)
            & (DatasetConfig.fides_key == fides_key)
        ),
    ).first()

    warnings = []

    if not fides_key:
        warnings.append("A fides_key was not found for this SaaS config.")

    if dataset:
        warnings.append(
            f"Must delete the dataset with fides_key '{fides_key}' before deleting this SaaS config."
        )

    # The secrets must be cleared since the SaaS config is used for validation and the secrets
    # might not pass validation once a new SaaS config is added.
    if connection_config.secrets:
        warnings.append(
            "Must clear the secrets from this connection config before deleting the SaaS config."
        )

    if warnings:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=" ".join(warnings))

    logger.info("Deleting SaaS config for connection '{}'", connection_config.key)
    connection_config.update(db, data={"saas_config": None})


@router.get(
    AUTHORIZE,
    dependencies=[Security(verify_oauth_client, scopes=[CONNECTION_AUTHORIZE])],
    response_model=str,
)
def authorize_connection(
    db: Session = Depends(deps.get_db),
    connection_config: ConnectionConfig = Depends(_get_saas_connection_config),
) -> Optional[str]:
    """Returns the authorization URL for the SaaS Connector (if available)"""

    verify_oauth_connection_config(connection_config)
    authentication = connection_config.get_saas_config().client_config.authentication  # type: ignore

    try:
        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = AuthenticationStrategy.get_strategy(
            authentication.strategy, authentication.configuration  # type: ignore
        )
        return auth_strategy.get_authorization_url(db, connection_config)
    except FidesopsException as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post(
    SAAS_CONNECTOR_FROM_TEMPLATE,
    dependencies=[Security(verify_oauth_client, scopes=[SAAS_CONNECTION_INSTANTIATE])],
    response_model=SaasConnectionTemplateResponse,
)
def instantiate_connection_from_template(
    saas_connector_type: str,
    template_values: SaasConnectionTemplateValues,
    db: Session = Depends(deps.get_db),
) -> SaasConnectionTemplateResponse:
    """
    Creates a SaaS Connector and a SaaS Dataset from a template.

    Looks up the connector type in the SaaS connector registry and, if all required
    fields are provided, persists the associated connection config and dataset to the database.
    """

    registry: ConnectorRegistry = load_registry()
    connector_template: Optional[ConnectorTemplate] = registry.get_connector_template(
        saas_connector_type
    )
    if not connector_template:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"SaaS connector type '{saas_connector_type}' is not yet available in Fidesops. For a list of available SaaS connectors, refer to {CONNECTION_TYPES}.",
        )

    if DatasetConfig.filter(
        db=db,
        conditions=(DatasetConfig.fides_key == template_values.instance_key),  # type: ignore[arg-type]
    ).count():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"SaaS connector instance key '{template_values.instance_key}' already exists.",
        )

    try:
        connection_config: ConnectionConfig = (
            create_connection_config_from_template_no_save(
                db, connector_template, template_values
            )
        )
    except KeyOrNameAlreadyExists as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=exc.args[0],
        )

    connection_config.secrets = validate_secrets(
        db, template_values.secrets, connection_config
    ).dict()
    connection_config.save(db=db)  # Not persisted to db until secrets are validated

    try:
        dataset_config: DatasetConfig = upsert_dataset_config_from_template(
            db, connection_config, connector_template, template_values
        )
    except Exception:
        connection_config.delete(db)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SaaS Connector could not be created from the '{saas_connector_type}' template at this time.",
        )
    logger.info(
        "SaaS Connector and Dataset {} successfully created from '{}' template.",
        template_values.instance_key,
        saas_connector_type,
    )
    return SaasConnectionTemplateResponse(
        connection=connection_config, dataset=dataset_config.dataset
    )


@router.post(
    REGISTER_CONNECTOR_TEMPLATE,
    dependencies=[Security(verify_oauth_client, scopes=[CONNECTOR_TEMPLATE_REGISTER])],
)
async def register_custom_connector_template(
    connector_template: UploadFile,
    db: Session = Depends(deps.get_db),
) -> None:
    """
    Accepts a connector template bundle, a zip file containing a
    SaaS config, dataset, and other files used to define a connector template

    The steps to register a connector template are as follows:

    1) Iterate through each file inside the zip file and look for certain files by name
    2) Persist the template to the database in the custom connector template table
    3) Register the template in the connector registry for immediate use

    On server startup, the connector registry will load all the connectors defined in this repo
    along with all the custom connector templates defined in the database
    """
    contents = await connector_template.read()
    zip_file = BytesIO(contents)

    # # Open the file as a zip file
    try:
        with zipfile.ZipFile(zip_file, "r") as zip_obj:
            # Iterate over the entries in the zip file
            for info in zip_obj.infolist():
                file_contents = zip_obj.read(info).decode()
                if info.filename.endswith("config.yml"):
                    config_contents = file_contents
                elif info.filename.endswith("dataset.yml"):
                    dataset_contents = file_contents
                elif info.filename.endswith("functions.py"):
                    function_contents = file_contents

            saas_config = SaaSConfig(**load_config_from_string(config_contents))
            template = CustomConnectorTemplate(
                key=saas_config.type,
                name=saas_config.name,
                config=config_contents,
                dataset=dataset_contents,
                icon=None,
                functions=function_contents,
            )
            template.save(db=db)
            registry = load_registry(db=db)
            registry.register_template(
                saas_config.type,
                ConnectorTemplate(
                    config=config_contents,
                    dataset=dataset_contents,
                    icon=None,
                    human_readable=saas_config.name,
                ),
            )
            register_custom_functions(function_contents)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid zip file")
