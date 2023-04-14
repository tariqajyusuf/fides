from typing import Dict

from fastapi import Depends, HTTPException, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from fideslang.models import System as SystemSchema
from loguru import logger as log
from pydantic.types import conlist
from sqlalchemy import insert
from sqlalchemy import update as _update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from fides.api.ctl.database.crud import (
    create_resource,
    delete_resource,
    get_resource,
    update_resource,
)
from fides.api.ctl.database.session import get_async_db
from fides.api.ctl.sql_models import (  # type: ignore[attr-defined]
    PrivacyDeclaration,
    System,
)
from fides.api.ctl.utils.api_router import APIRouter
from fides.api.ops.api import deps
from fides.api.ops.api.v1 import scope_registry
from fides.api.ops.api.v1.scope_registry import (
    CONNECTION_CREATE_OR_UPDATE,
    CONNECTION_READ,
    SYSTEM_CREATE,
)
from fides.api.ops.api.v1.urn_registry import SYSTEM_CONNECTIONS, V1_URL_PREFIX
from fides.api.ops.models.connectionconfig import ConnectionConfig
from fides.api.ops.schemas.connection_configuration.connection_config import (
    BulkPutConnectionConfiguration,
    ConnectionConfigurationResponse,
    CreateConnectionConfigurationWithSecrets,
)
from fides.api.ops.util.connection_util import patch_connection_configs
from fides.api.ops.util.oauth_util import verify_oauth_client, verify_oauth_client_prod
from fides.api.ops.util.system_manager_oauth_util import (
    verify_oauth_client_for_system_from_fides_key_cli,
    verify_oauth_client_for_system_from_request_body_cli,
)

system_router = APIRouter(tags=["System"], prefix=f"{V1_URL_PREFIX}/system")
system_connections_router = APIRouter(
    tags=["System"], prefix=f"{V1_URL_PREFIX}{SYSTEM_CONNECTIONS}"
)


def get_system(db: Session, fides_key: str) -> System:
    system = System.get_by(db, field="fides_key", value=fides_key)
    if system is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="A valid system must be provided to create or update connections",
        )
    return system


@system_connections_router.get(
    "",
    dependencies=[Security(verify_oauth_client, scopes=[CONNECTION_READ])],
    status_code=HTTP_200_OK,
    response_model=Page[ConnectionConfigurationResponse],
)
def get_system_connections(
    fides_key: str, params: Params = Depends(), db: Session = Depends(deps.get_db)
) -> AbstractPage[ConnectionConfigurationResponse]:
    """
    Return all the connection configs related to a system.
    """
    system = get_system(db, fides_key)
    query = ConnectionConfig.query(db)
    query = query.filter(ConnectionConfig.system_id == system.id)
    return paginate(query.order_by(ConnectionConfig.name.asc()), params=params)


@system_connections_router.patch(
    "",
    dependencies=[Security(verify_oauth_client, scopes=[CONNECTION_CREATE_OR_UPDATE])],
    status_code=HTTP_200_OK,
    response_model=BulkPutConnectionConfiguration,
)
def patch_connections(
    fides_key: str,
    configs: conlist(CreateConnectionConfigurationWithSecrets, max_items=50),  # type: ignore
    db: Session = Depends(deps.get_db),
) -> BulkPutConnectionConfiguration:
    """
    Given a valid System fides key, a list of connection config data elements, optionally
    containing the secrets, create or update corresponding ConnectionConfig objects or report
    failure.

    If the key in the payload exists, it will be used to update an existing ConnectionConfiguration.
    Otherwise, a new ConnectionConfiguration will be created for you.
    """
    system = get_system(db, fides_key)
    return patch_connection_configs(db, configs, system)


@system_router.put(
    "/",
    response_model=SystemSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "error": "user does not have permission to modify this resource",
                            "resource_type": "system",
                            "fides_key": "example.key",
                        }
                    }
                }
            }
        },
    },
)
async def update(
    resource: SystemSchema = Security(
        verify_oauth_client_for_system_from_request_body_cli,
        scopes=[scope_registry.SYSTEM_UPDATE],
    ),  # Security dependency defined here instead of the path operation decorator so we have access to the request body
    # to be able to look up the system as well as return a value
    db: AsyncSession = Depends(get_async_db),
) -> Dict:
    """
    Update a System by the fides_key extracted from the request body.  Defined outside of the crud routes
    to add additional "system manager" permission checks.
    """
    system: System = await get_resource(
        sql_model=System, fides_key=resource.fides_key, async_session=db
    )

    declaration_by_data_use: dict[str, PrivacyDeclaration] = {}
    # map existing declarations by their data use
    for existing_declaration in system.privacy_declarations:
        declaration_by_data_use[existing_declaration.data_use] = existing_declaration

    try:
        async with db.begin():
            # now iterate through declarations specified on the request
            for privacy_declaration in resource.privacy_declarations:
                data = privacy_declaration.dict()
                data["system_id"] = resource.fides_key  # add FK back to system

                # if the system already has a declaration with the data use
                # then use its ID to update the declaration record in place
                if existing_declaration := declaration_by_data_use.get(
                    privacy_declaration.data_use, None
                ):
                    # remove the existing item to indicate it was specified in the update
                    declaration_by_data_use.pop(privacy_declaration.data_use)
                    # update the declaration in place
                    await db.execute(
                        _update(PrivacyDeclaration)
                        .where(PrivacyDeclaration.id == existing_declaration.id)
                        .values(data)
                    )

                else:  # otherwise, create the declaration
                    query = insert(PrivacyDeclaration).values(data)
                    await db.execute(query)

            # any declarations that remain here should be deleted, as they were
            # not specified  on the upsert request
            for existing_declaration in declaration_by_data_use.values():
                await db.delete(existing_declaration)
    except Exception as e:
        log.error(
            f"Error adding privacy declarations, reverting system creation: {str(e)}"
        )
        raise e

    delattr(
        resource, "privacy_declarations"
    )  # remove the attribute on the system since we've already updated declarations

    # perform any updates on the system resource itself
    updated_system = await update_resource(System, resource.dict(), db)
    async with db.begin():
        await db.refresh(updated_system)
    return updated_system


@system_router.delete(
    "/{fides_key}",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "error": "user does not have permission to modify this resource",
                            "resource_type": "system",
                            "fides_key": "example.key",
                        }
                    }
                }
            }
        },
    },
)
async def delete(
    fides_key: str = Security(
        verify_oauth_client_for_system_from_fides_key_cli,
        scopes=[scope_registry.SYSTEM_DELETE],
    ),  # Security dependency defined here instead of the path operation decorator so we have access to the fides_key
    # to retrieve the System and also return a value
    db: AsyncSession = Depends(get_async_db),
) -> Dict:
    """
    Delete a System by its fides_key. Defined outside of the crud routes
    to add additional "system manager" permission checks.
    """
    deleted_resource = await delete_resource(System, fides_key, db)
    # Convert the resource to a dict explicitly for the response
    deleted_resource_dict = SystemSchema.from_orm(deleted_resource).dict()
    return {
        "message": "resource deleted",
        "resource": deleted_resource_dict,
    }


@system_router.post(
    "/",
    response_model=SystemSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Security(
            verify_oauth_client_prod,
            scopes=[SYSTEM_CREATE],
        )
    ],
)
async def create(
    resource: SystemSchema,
    db: AsyncSession = Depends(get_async_db),
) -> Dict:
    """
    Override `System` create/POST to handle `.privacy_declarations` defined inline,
    for backward compatibility and ease of use for API users.
    """
    # copy out the declarations to be stored separately
    # as they will be processed AFTER the system is added
    privacy_declarations = resource.privacy_declarations

    # remove the attribute on the system update since the declarations will be created separately
    delattr(resource, "privacy_declarations")

    # create the system resource using generic creation
    # the system must be created before the privacy declarations so that it can be referenced
    created_system = await create_resource(
        System, resource_dict=resource.dict(), async_session=db
    )

    privacy_declaration_exception = None
    try:
        async with db.begin():
            # create the specified declarations as records in their own table
            for privacy_declaration in privacy_declarations:
                data = privacy_declaration.dict()
                data["system_id"] = resource.fides_key  # add FK back to system
                PrivacyDeclaration.create(
                    db, data=data
                )  # create the associated PrivacyDeclaration
    except Exception as e:
        privacy_declaration_exception = e

    if privacy_declaration_exception:
        log.error(
            f"Error adding privacy declarations, reverting system creation: {str(privacy_declaration_exception)}"
        )
        async with db.begin():
            await db.delete(created_system)
        raise privacy_declaration_exception

    async with db.begin():
        await db.refresh(created_system)

    return created_system
