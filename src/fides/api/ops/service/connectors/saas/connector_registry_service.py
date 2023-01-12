from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_loader
from types import ModuleType
from typing import Dict, Iterable, List, Optional, Tuple, Union

from loguru import logger
from packaging.version import LegacyVersion, Version
from packaging.version import parse as parse_version
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from toml import load as load_toml

from fides.api.ops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fides.api.ops.models.custom_connector_template import CustomConnectorTemplate
from fides.api.ops.models.datasetconfig import DatasetConfig
from fides.api.ops.schemas.connection_configuration.connection_config import (
    SaasConnectionTemplateValues,
)
from fides.api.ops.schemas.dataset import FidesopsDataset
from fides.api.ops.schemas.saas.saas_config import SaaSConfig
from fides.api.ops.util.saas_util import (
    load_config_from_string,
    load_dataset_from_string,
    load_yaml_as_string,
    replace_config_placeholders,
    replace_dataset_placeholders,
)

_registry: Optional["ConnectorRegistry"] = None
registry_file = "data/saas/saas_connector_registry.toml"


class ConnectorTemplate(BaseModel):
    """
    A collection of artifacts that make up a complete SaaS connector (SaaS config, dataset, etc.)
    """

    config: str
    dataset: str
    icon: str
    human_readable: str

    @validator("config")
    def validate_config(cls, config: str) -> str:
        """Validates the config"""
        SaaSConfig(**load_config_from_string(config))
        return config

    @validator("dataset")
    def validate_dataset(cls, dataset: str) -> str:
        """Validates the dataset at the given path"""
        FidesopsDataset(**load_dataset_from_string(dataset))
        return dataset


class ConnectorRegistry(BaseModel):
    """A map of SaaS connector templates"""

    registry: Dict[str, ConnectorTemplate] = {}

    def connector_types(self) -> List[str]:
        """List of registered SaaS connector types"""
        return list(self.registry)

    def get_connector_template(
        self, connector_type: str
    ) -> Optional[ConnectorTemplate]:
        """
        Returns an object containing the references to the various SaaS connector artifacts
        """
        return self.registry.get(connector_type)

    def register_template(
        self, connector_type: str, template: ConnectorTemplate
    ) -> None:
        self.registry[connector_type] = template


def create_connection_config_from_template_no_save(
    db: Session,
    template: ConnectorTemplate,
    template_values: SaasConnectionTemplateValues,
) -> ConnectionConfig:
    """Creates a SaaS connection config from a template without saving it."""
    # Load saas config from template and replace every instance of "<instance_fides_key>" with the fides_key
    # the user has chosen
    config_from_template: Dict = replace_config_placeholders(
        template.config, "<instance_fides_key>", template_values.instance_key
    )

    # Create SaaS ConnectionConfig
    connection_config = ConnectionConfig.create_without_saving(
        db,
        data={
            "name": template_values.name,
            "key": template_values.key,
            "description": template_values.description,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "saas_config": config_from_template,
        },
    )

    return connection_config


def upsert_dataset_config_from_template(
    db: Session,
    connection_config: ConnectionConfig,
    template: ConnectorTemplate,
    template_values: SaasConnectionTemplateValues,
) -> DatasetConfig:
    """
    Creates a `DatasetConfig` from a template
    and associates it with a ConnectionConfig.
    If the `DatasetConfig` already exists in the db,
    then the existing record is updated.
    """
    # Load the dataset config from template and replace every instance of "<instance_fides_key>" with the fides_key
    # the user has chosen
    dataset_from_template: Dict = replace_dataset_placeholders(
        template.dataset, "<instance_fides_key>", template_values.instance_key
    )

    data = {
        "connection_config_id": connection_config.id,
        "fides_key": template_values.instance_key,
        "dataset": dataset_from_template,
    }
    dataset_config = DatasetConfig.create_or_update(db, data=data)
    return dataset_config


def load_registry(db: Session = None) -> ConnectorRegistry:
    """Populates the connector registry with templates specified in the filesystem and the database"""
    global _registry  # pylint: disable=W0603
    if _registry is None:
        _registry = ConnectorRegistry()
        for connector_type, entry in load_toml(registry_file).items():
            # register the config and dataset
            config = load_yaml_as_string(entry["config"])
            dataset = load_yaml_as_string(entry["dataset"])
            _registry.register_template(
                connector_type,
                ConnectorTemplate(
                    config=config,
                    dataset=dataset,
                    icon=entry["icon"],
                    human_readable=entry["human_readable"],
                ),
            )
            # register custom functions if available
            custom_functions = entry.get("custom_functions")
            if custom_functions:
                with open(custom_functions) as file:
                    contents = file.read()
                    register_custom_functions(contents)
                    logger.info(f"Loaded custom functions from {file.name}")
        if db:
            for template in CustomConnectorTemplate.all(db=db):
                _registry.register_template(
                    template.key,
                    ConnectorTemplate(
                        config=template.config,
                        dataset=template.dataset,
                        icon=template.icon,
                        human_readable=template.name,
                    ),
                )
                # register custom functions if available
                if template.functions:
                    register_custom_functions(template.functions)
                    logger.info(
                        "Loaded custom functions from the custom connector template '%s'",
                        template.key,
                    )
    return _registry


def update_saas_configs(db: Session) -> None:
    """
    Updates SaaS config instances currently in the DB if to the
    corresponding template in the registry are found.

    Effectively an "update script" for SaaS config instances,
    to be run on server bootstrap.
    """
    assert _registry, "SaaS connector template registry has not been loaded"
    for connector_type in _registry.connector_types():
        logger.debug(
            "Determining if any updates are needed for connectors of type {} based on templates...",
            connector_type,
        )
        template: ConnectorTemplate = _registry.get_connector_template(  # type: ignore
            connector_type
        )
        saas_config = SaaSConfig(**load_config_from_string(template.config))
        template_version: Union[LegacyVersion, Version] = parse_version(
            saas_config.version
        )

        connection_configs: Iterable[ConnectionConfig] = ConnectionConfig.filter(
            db=db,
            conditions=(ConnectionConfig.saas_config["type"].astext == connector_type),
        ).all()
        for connection_config in connection_configs:
            saas_config_instance = SaaSConfig.parse_obj(connection_config.saas_config)
            if parse_version(saas_config_instance.version) < template_version:
                logger.info(
                    "Updating SaaS config instance '{}' of type '{}' as its version, {}, was found to be lower than the template version {}",
                    saas_config_instance.fides_key,
                    connector_type,
                    saas_config_instance.version,
                    template_version,
                )
                try:
                    update_saas_instance(
                        db,
                        connection_config,
                        template,
                        saas_config_instance,
                    )
                except Exception:
                    logger.error(
                        "Encountered error attempting to update SaaS config instance {}",
                        saas_config_instance.fides_key,
                        exc_info=True,
                    )


def update_saas_instance(
    db: Session,
    connection_config: ConnectionConfig,
    template: ConnectorTemplate,
    saas_config_instance: SaaSConfig,
) -> None:
    """
    Replace in the DB the existing SaaS instance configuration data
    (SaaSConfig, DatasetConfig) associated with the given ConnectionConfig
    with new instance configuration data based on the given ConnectorTemplate
    """
    template_vals = SaasConnectionTemplateValues(
        name=connection_config.name,
        key=connection_config.key,
        description=connection_config.description,
        secrets=connection_config.secrets,
        instance_key=saas_config_instance.fides_key,
    )

    config_from_template: Dict = replace_config_placeholders(
        template.config, "<instance_fides_key>", template_vals.instance_key
    )

    connection_config.update_saas_config(db, SaaSConfig(**config_from_template))

    upsert_dataset_config_from_template(db, connection_config, template, template_vals)


def register_custom_functions(script: str) -> None:
    class StringLoader(Loader):
        """Custom import loader to load code from a string"""

        def __init__(self, source_string: str) -> None:
            self.source_string = source_string

        def get_code(self, _: str) -> Tuple[str, str, str]:
            return self.source_string, "<string>", "exec"

        def exec_module(self, module: ModuleType) -> None:
            exec(self.source_string, module.__dict__)

        def get_filename(self, _: str) -> str:
            return "<string>"

        def is_package(self, _: str) -> bool:
            return False

    loader = StringLoader(script)

    module_spec = spec_from_loader("custom_connector_functions", loader)
    if module_spec:
        module = module_from_spec(module_spec)
        loader.exec_module(module)
