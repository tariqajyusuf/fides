from typing import Callable, Dict
from unittest import mock
from unittest.mock import Mock

import yaml
from sqlalchemy.orm import Session

from fides.api.ops.models.datasetconfig import DatasetConfig
from fides.api.ops.service.authentication import authentication_strategy_factory
from fides.api.ops.service.connectors.saas.connector_registry_service import (
    ConnectorTemplate,
    load_registry,
    register_custom_functions,
    update_saas_configs,
)
from fides.api.ops.service.saas_request.saas_request_override_factory import (
    SaaSRequestOverrideFactory,
    SaaSRequestType,
)
from fides.api.ops.util.saas_util import (
    load_config_from_string,
    load_dataset_from_string,
    load_yaml_as_string,
)

NEW_CONFIG_DESCRIPTION = "new test config description"
NEW_DATASET_DESCRIPTION = "new test dataset description"
NEW_CONNECTOR_PARAM = {"name": "new_param", "default_value": "new_param_default_value"}
NEW_ENDPOINT = {
    "name": "new endpoint",
    "requests": {
        "read": {
            "method": "GET",
            "path": "/test/path",
            "param_values": [{"name": "test_param", "identity": "email"}],
        }
    },
}
NEW_FIELD = {
    "name": "new_field",
    "data_categories": ["system.operations"],
}
NEW_COLLECTION = {
    "name": "new_collection",
    "fields": [NEW_FIELD],
}


class TestConnectionRegistry:
    def test_get_connector_template(self, db: Session):
        registry = load_registry(db=db)

        assert "mailchimp" in registry.connector_types()

        assert registry.get_connector_template("bad_key") is None
        mailchimp_registry = registry.get_connector_template("mailchimp")

        assert mailchimp_registry == ConnectorTemplate(
            config=load_yaml_as_string("data/saas/config/mailchimp_config.yml"),
            dataset=load_yaml_as_string("data/saas/dataset/mailchimp_dataset.yml"),
            icon="data/saas/icon/mailchimp.svg",
            human_readable="Mailchimp",
        )

    @mock.patch(
        "fides.api.ops.service.connectors.saas.connector_registry_service.replace_dataset_placeholders"
    )
    @mock.patch(
        "fides.api.ops.service.connectors.saas.connector_registry_service.replace_config_placeholders"
    )
    @mock.patch(
        "fides.api.ops.service.connectors.saas.connector_registry_service.load_config_from_string"
    )
    def test_update_config_additions(
        self,
        load_config_from_string_mock_object: Mock,
        replace_config_placeholders_mock_object: Mock,
        replace_dataset_placeholders_mock_object: Mock,
        db,
        secondary_mailchimp_instance,
        tertiary_mailchimp_instance,
        secondary_sendgrid_instance,
    ):
        update_config(
            load_config_from_string_mock_object,
            load_config_from_string_mocked_additions_function,
            replace_config_placeholders_mock_object,
            replace_config_placeholders_mocked_additions_function,
            replace_dataset_placeholders_mock_object,
            replace_dataset_placeholders_mocked_additions_function,
            validate_updated_instances_additions,
            db,
            secondary_mailchimp_instance,
            tertiary_mailchimp_instance,
            secondary_sendgrid_instance,
        )

    @mock.patch(
        "fides.api.ops.service.connectors.saas.connector_registry_service.replace_dataset_placeholders"
    )
    @mock.patch(
        "fides.api.ops.service.connectors.saas.connector_registry_service.replace_config_placeholders"
    )
    @mock.patch(
        "fides.api.ops.service.connectors.saas.connector_registry_service.load_config_from_string"
    )
    def test_update_config_removals(
        self,
        load_config_from_string_mock_object: Mock,
        replace_config_placeholders_mock_object: Mock,
        replace_dataset_placeholders_mock_object: Mock,
        db,
        secondary_mailchimp_instance,
        tertiary_mailchimp_instance,
        secondary_sendgrid_instance,
    ):
        update_config(
            load_config_from_string_mock_object,
            load_config_from_string_mocked_removals_function,
            replace_config_placeholders_mock_object,
            replace_config_placeholders_mocked_removals_function,
            replace_dataset_placeholders_mock_object,
            rename_dataset_mocked_removals_function,
            validate_updated_instances_removals,
            db,
            secondary_mailchimp_instance,
            tertiary_mailchimp_instance,
            secondary_sendgrid_instance,
        )


class TestCustomFunctionLoading:
    def test_load_custom_override_functions(self):
        script = """
from json import dumps
from typing import Any, Dict, List

from requests import put

from fides.api.ops.common_exceptions import (
    ClientUnsuccessfulException,
    ConnectionException,
)
from fides.api.ops.models.policy import Policy
from fides.api.ops.models.privacy_request import PrivacyRequest
from fides.api.ops.service.saas_request.saas_request_override_factory import (
    SaaSRequestType,
    register,
)
from fides.api.ops.util.saas_util import PRIVACY_REQUEST_ID
from fides.core.config import get_config

CONFIG = get_config()

@register("momo_user_update", [SaaSRequestType.UPDATE])
def momo_user_update(
    param_values_per_row: List[Dict[str, Any]],
    policy: Policy,
    privacy_request: PrivacyRequest,
    secrets: Dict[str, Any],
) -> int:
    rows_updated: int = 0
    return rows_updated
        """
        register_custom_functions(script)
        custom_function: Callable = SaaSRequestOverrideFactory.get_override(
            "momo_user_update", SaaSRequestType.UPDATE
        )
        assert custom_function.__name__ == "momo_user_update"

    def test_load_custom_strategy(self):
        script = '''
import math
import time
from typing import Any, Dict, Optional

import jwt.utils
from requests import PreparedRequest

from fides.api.ops.models.connectionconfig import ConnectionConfig
from fides.api.ops.schemas.saas.strategy_configuration import StrategyConfiguration
from fides.api.ops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fides.api.ops.util.saas_util import assign_placeholders


class DoorsmashAuthenticationConfiguration(StrategyConfiguration):
    """
    Parameters to generate a Doorsmash JWT token
    """


class DoorsmashAuthenticationStrategy(AuthenticationStrategy):
    """
    Adds a Doorsmash JWT as bearer auth to the request
    """

    name = "doorsmash"
    configuration_model = DoorsmashAuthenticationConfiguration

    def __init__(self, configuration: DoorsmashAuthenticationConfiguration):
        pass

    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """
        Generate a Doorsmash JWT and add it as bearer auth
        """

        secrets: Optional[Dict[str, Any]] = connection_config.secrets

        token = jwt.encode(
            {
                "aud": "doorsmash",
                "iss": assign_placeholders(self.developer_id, secrets)
                if secrets
                else None,
                "kid": assign_placeholders(self.key_id, secrets) if secrets else None,
                "exp": str(math.floor(time.time() + 60)),
                "iat": str(math.floor(time.time())),
            },
            jwt.utils.base64url_decode(
                assign_placeholders(self.signing_secret, secrets)  # type: ignore
            ),
            algorithm="HS256",
            headers={"dd-ver": "DD-JWT-V1"},
        )

        request.headers["Authorization"] = f"Bearer {token}"
        return request  
'''
        register_custom_functions(script)
        assert "doorsmash" in authentication_strategy_factory.get_strategy_names()


def update_config(
    load_config_from_string_mock_object,
    load_config_from_string_mock_function: Callable,
    replace_config_placeholders_mock_object,
    replace_config_placeholders_mock_function: Callable,
    replace_dataset_placeholders_mock_object,
    replace_dataset_placeholders_mock_function: Callable,
    validation_function: Callable,
    db,
    secondary_mailchimp_instance,
    tertiary_mailchimp_instance,
    secondary_sendgrid_instance,
):
    """
    Helper function to test config updates.

    First, load the original templates for `mailchimp` and `sendgrid`,
    and instantiate two `mailchimp` instances and one `sendgrid` instance
    by means of fixtures. We use these 3 instances to test functionality
    across multiple instances of the same type, as well as multiple types.

    Then, based on the provided mock objects and functions to override,
    "updates" are made to connector templates for `mailchimp` and `sendgrid`.
    The nature of those updates are "plugged in" via the override functions.

    Then, perform the update "script", i.e. invoke `update_saas_configs`.

    Then, confirm that the instances have been updated as expected, by
    invoking a plugged-in `validation_function`
    """
    registry = load_registry()
    assert "mailchimp" in registry.connector_types()

    mailchimp_template_config = load_config_from_string(
        registry.get_connector_template("mailchimp").config
    )
    mailchimp_template_dataset = load_dataset_from_string(
        registry.get_connector_template("mailchimp").dataset
    )

    mailchimp_version = mailchimp_template_config["version"]

    sendgrid_template_config = load_config_from_string(
        registry.get_connector_template("sendgrid").config
    )
    sendgrid_template_dataset = load_dataset_from_string(
        registry.get_connector_template("sendgrid").dataset
    )
    sendgrid_version = sendgrid_template_config["version"]

    # confirm original version of template works as expected
    (
        secondary_mailchimp_config,
        secondary_mailchimp_dataset,
    ) = secondary_mailchimp_instance
    secondary_mailchimp_saas_config = secondary_mailchimp_config.saas_config
    secondary_mailchimp_dataset.dataset["description"] = mailchimp_template_dataset[
        "description"
    ]
    assert secondary_mailchimp_saas_config["version"] == mailchimp_version
    assert (
        secondary_mailchimp_saas_config["description"]
        == mailchimp_template_config["description"]
    )

    (
        tertiary_mailchimp_config,
        tertiary_mailchimp_dataset,
    ) = tertiary_mailchimp_instance
    tertiary_mailchimp_saas_config = tertiary_mailchimp_config.saas_config
    tertiary_mailchimp_dataset.dataset["description"] = mailchimp_template_dataset[
        "description"
    ]
    tertiary_mailchimp_saas_config = (
        tertiary_mailchimp_dataset.connection_config.saas_config
    )
    assert tertiary_mailchimp_saas_config["version"] == mailchimp_version
    assert (
        tertiary_mailchimp_saas_config["description"]
        == mailchimp_template_config["description"]
    )

    (
        secondary_sendgrid_config,
        secondary_sendgrid_dataset,
    ) = secondary_sendgrid_instance
    secondary_sendgrid_saas_config = secondary_sendgrid_config.saas_config
    secondary_sendgrid_dataset.dataset["description"] = sendgrid_template_dataset[
        "description"
    ]
    assert secondary_sendgrid_saas_config["version"] == sendgrid_version
    assert (
        secondary_sendgrid_saas_config["description"]
        == sendgrid_template_config["description"]
    )

    # mock methods within template instantiation workflow
    # to produce an updated saas config template
    # this mimics "updates" made to SaaS config and dataset templates
    # for mailchimp and sendgrid
    load_config_from_string_mock_object.side_effect = (
        load_config_from_string_mock_function
    )
    replace_config_placeholders_mock_object.side_effect = (
        replace_config_placeholders_mock_function
    )
    replace_dataset_placeholders_mock_object.side_effect = (
        replace_dataset_placeholders_mock_function
    )

    # run update "script"
    update_saas_configs(db)

    # confirm updates applied successfully
    secondary_mailchimp_dataset: DatasetConfig = DatasetConfig.filter(
        db=db,
        conditions=DatasetConfig.fides_key == secondary_mailchimp_dataset.fides_key,
    ).first()
    validation_function(
        secondary_mailchimp_dataset,
        mailchimp_template_config,
        mailchimp_template_dataset,
        secondary_mailchimp_config.key,
        secondary_mailchimp_dataset.fides_key,
    )

    tertiary_mailchimp_dataset: DatasetConfig = DatasetConfig.filter(
        db=db,
        conditions=DatasetConfig.fides_key == tertiary_mailchimp_dataset.fides_key,
    ).first()
    validation_function(
        tertiary_mailchimp_dataset,
        mailchimp_template_config,
        mailchimp_template_dataset,
        tertiary_mailchimp_config.key,
        tertiary_mailchimp_dataset.fides_key,
    )

    secondary_sendgrid_dataset: DatasetConfig = DatasetConfig.filter(
        db=db,
        conditions=DatasetConfig.fides_key == secondary_sendgrid_dataset.fides_key,
    ).first()
    validation_function(
        secondary_sendgrid_dataset,
        sendgrid_template_config,
        sendgrid_template_dataset,
        secondary_sendgrid_config.key,
        secondary_sendgrid_dataset.fides_key,
    )

    # clean up after ourselves
    secondary_mailchimp_config.delete(db)
    tertiary_mailchimp_config.delete(db)
    secondary_sendgrid_config.delete(db)


def increment_ver(version):
    version = version.split(".")
    version[2] = str(int(version[2]) + 1)
    return ".".join(version)


### Additions helpers ###


def load_config_from_string_mocked_additions_function(config_string: str) -> Dict:
    """
    Loads the saas config from the yaml file
    Mocked to make additions to mailchimp config template _only_ for testing
    """
    config = yaml.safe_load(config_string).get("saas_config", [])
    update_config_additions(config)
    return config


def replace_config_placeholders_mocked_additions_function(
    config_string: str, string_to_replace: str, replacement: str
) -> Dict:
    """
    Loads the saas config from the yaml file and replaces any string with the given value
    Mocked to make additions to mailchimp config template _only_ for testing
    """
    yaml_str: str = config_string.replace(string_to_replace, replacement)
    config: Dict = yaml.safe_load(yaml_str).get("saas_config", [])
    update_config_additions(config)
    return config


def update_config_additions(config: Dict):
    if config["type"] in ("mailchimp", "sendgrid"):
        config["version"] = increment_ver(config["version"])
        config["description"] = NEW_CONFIG_DESCRIPTION
        config["connector_params"].append(NEW_CONNECTOR_PARAM)
        config["endpoints"].append(NEW_ENDPOINT)


def replace_dataset_placeholders_mocked_additions_function(
    dataset_string: str, string_to_replace: str, replacement: str
) -> Dict:
    """
    Loads the dataset from the yaml file and replaces any string with the given value
    Mocked to make additions to mailchimp dataset template _only_ for testing
    """
    yaml_str: str = dataset_string.replace(string_to_replace, replacement)
    dataset: Dict = yaml.safe_load(yaml_str).get("dataset", [])[0]
    if dataset["name"] in (
        "Mailchimp Dataset",
        "Sendgrid Dataset",
    ):
        dataset["description"] = NEW_DATASET_DESCRIPTION
        dataset["collections"][0]["fields"].append(NEW_FIELD)
        dataset["collections"].append(NEW_COLLECTION)
    return dataset


def validate_updated_instances_additions(
    updated_dataset_config: DatasetConfig,
    original_template_config: Dict,
    original_template_dataset: Dict,
    key: str,
    fides_key: str,
):
    # check for dataset additions to template
    assert updated_dataset_config.dataset["description"] == NEW_DATASET_DESCRIPTION
    assert (
        len(updated_dataset_config.dataset["collections"])
        == len(original_template_dataset["collections"]) + 1
    )
    assert NEW_COLLECTION in updated_dataset_config.dataset["collections"]
    assert NEW_FIELD in updated_dataset_config.dataset["collections"][0]["fields"]

    # check for config additions to template
    updated_saas_config = updated_dataset_config.connection_config.saas_config
    assert updated_saas_config["version"] == increment_ver(
        original_template_config["version"]
    )
    assert updated_saas_config["description"] == NEW_CONFIG_DESCRIPTION
    assert any(
        NEW_CONNECTOR_PARAM["name"] == param["name"]
        for param in updated_saas_config["connector_params"]
    )
    assert (
        len(updated_saas_config["endpoints"])
        == len(original_template_config["endpoints"]) + 1
    )
    assert any(
        NEW_ENDPOINT["name"] == endpoint["name"]
        for endpoint in updated_saas_config["endpoints"]
    )

    assert updated_dataset_config.connection_config.key == key
    assert updated_saas_config["fides_key"] == fides_key


### Removals helpers ###


def load_config_from_string_mocked_removals_function(config_string: str) -> Dict:
    """
    Loads the saas config from the yaml file
    Mocked to make removals to mailchimp config template _only_ for testing
    """
    config = yaml.safe_load(config_string).get("saas_config", [])
    update_config_removals(config)
    return config


def replace_config_placeholders_mocked_removals_function(
    config_string: str, string_to_replace: str, replacement: str
) -> Dict:
    """
    Loads the saas config from the yaml file and replaces any string with the given value
    Mocked to make removals to mailchimp config template _only_ for testing
    """
    yaml_str: str = config_string.replace(string_to_replace, replacement)
    config: Dict = yaml.safe_load(yaml_str).get("saas_config", [])
    update_config_removals(config)
    return config


def update_config_removals(config: Dict):
    if config["type"] in (
        "mailchimp",
        "sendgrid",
    ):
        config["version"] = increment_ver(config["version"])
        config["endpoints"].pop()
        config["connector_params"].pop()


def rename_dataset_mocked_removals_function(
    dataset_string: str, string_to_replace: str, replacement: str
) -> Dict:
    """
    Loads the dataset from the yaml file and replaces any string with the given value
    Mocked to make removals to mailchimp dataset _only_ for testing
    """
    yaml_str: str = dataset_string.replace(string_to_replace, replacement)
    dataset: Dict = yaml.safe_load(yaml_str).get("dataset", [])[0]
    if dataset["name"] in (
        "Mailchimp Dataset",
        "Sendgrid Dataset",
    ):
        dataset["collections"].pop()
    return dataset


def validate_updated_instances_removals(
    updated_dataset_config: DatasetConfig,
    original_template_config: Dict,
    original_template_dataset: Dict,
    key: str,
    fides_key: str,
):
    # check for dataset removals to template
    assert (
        len(updated_dataset_config.dataset["collections"])
        == len(original_template_dataset["collections"]) - 1
    )

    # check for config removals to template
    updated_saas_config = updated_dataset_config.connection_config.saas_config
    assert (
        len(updated_saas_config["endpoints"])
        == len(original_template_config["endpoints"]) - 1
    )
    assert (
        len(updated_saas_config["connector_params"])
        == len(original_template_config["connector_params"]) - 1
    )

    assert updated_dataset_config.connection_config.key == key
    assert updated_saas_config["fides_key"] == fides_key
