# pylint: disable=missing-docstring, redefined-outer-name

import pytest
from starlette.testclient import TestClient

from fidesapi.routes.util import API_PREFIX
from fidesctl.core.config import FidesctlConfig


@pytest.mark.integration
@pytest.mark.parametrize(
    "organization_fides_key, expected_status_code",
    [
        ("fake_organization", 404),
    ],
)
def test_datamap_failure(
    test_config: FidesctlConfig,
    organization_fides_key: str,
    expected_status_code: int,
    test_client: TestClient,
) -> None:
    response = test_client.get(
        test_config.cli.server_url + API_PREFIX + "/datamap/" + organization_fides_key,
        headers=test_config.user.request_headers,
    )
    assert response.status_code == expected_status_code
