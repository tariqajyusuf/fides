from typing import Any, Dict, Generator

import pydash
import pytest
import requests


from tests.ops.integration_tests.saas.connector_runner import (
    ConnectorRunner,
    generate_random_email,
)
from tests.ops.test_helpers.vault_client import get_secrets

secrets = get_secrets("sparkpost")


@pytest.fixture(scope="session")
def sparkpost_secrets(saas_config) -> Dict[str, Any]:
    return {
        "domain": pydash.get(saas_config, "sparkpost.domain")
        or secrets["domain"],
        "api_key": pydash.get(saas_config, "sparkpost.api_key")
        or secrets["api_key"]
    }


@pytest.fixture(scope="session")
def sparkpost_identity_email(saas_config) -> str:
    return (
        pydash.get(
            saas_config, "sparkpost.identity_email") or secrets["identity_email"]
    )


@pytest.fixture
def sparkpost_erasure_identity_email() -> str:
    return generate_random_email()


@pytest.fixture
def sparkpost_external_references() -> Dict[str, Any]:
    return {}


@pytest.fixture
def sparkpost_erasure_external_references() -> Dict[str, Any]:
    return {}

@pytest.fixture
def sparkpost_client(sparkpost_secrets) -> Generator:
    yield SparkpostClient(sparkpost_secrets)
    

class SparkpostClient:
    headers: object = {}
    base_url: str = ""
    def __init__(self, secrets: Dict[str, Any]):
        self.base_url = f"https://{secrets['domain']}"
        self.auth = secrets["api_key"], "123"

    def create_recipient(self, email):
        return requests.post(
            url=f"{self.base_url}/api/v1/recipient-lists",
            auth=self.auth,
            json={
                "name": "test recipient",
                "description": "Test request",
                "recipients": [
                    {
                        "address": {
                            "email": email,
                            "name": "Wilma"
                        },
                        "tags": [
                            "greeting",
                            "prehistoric",
                            "fred",
                            "flintstone"
                        ],
                        "metadata": {
                            "age": "24",
                            "place": "Bedrock"
                        },
                        "substitution_data": {
                            "favorite_color": "SparkPost Orange",
                            "job": "Software Engineer"
                        }
                    }
                ]
            }
        )

@pytest.fixture
def sparkpost_erasure_data(
    sparkpost_erasure_identity_email: str,
    sparkpost_client: SparkpostClient,
) -> Generator:
    
    # recipient
    response = sparkpost_client.create_recipient(sparkpost_erasure_identity_email)
    assert response.ok
    recipient = response.json()
    yield recipient


@pytest.fixture
def sparkpost_runner(
    db,
    cache,
    sparkpost_secrets,
    sparkpost_external_references,
    sparkpost_erasure_external_references,
) -> ConnectorRunner:
    return ConnectorRunner(
        db,
        cache,
        "sparkpost",
        sparkpost_secrets,
        external_references=sparkpost_external_references,
        erasure_external_references=sparkpost_erasure_external_references,
    )

