import random
import time

import pytest
import requests

from fides.api.ops.graph.graph import DatasetGraph
from fides.api.ops.models.privacy_request import PrivacyRequest
from fides.api.ops.schemas.redis_cache import Identity
from fides.api.ops.service.connectors import get_connector
from fides.api.ops.task import graph_task
from fides.api.ops.task.graph_task import get_cached_data_for_erasures
from fides.core.config import get_config
from tests.ops.graph.graph_test_util import assert_rows_match

CONFIG = get_config()


@pytest.mark.integration_saas
@pytest.mark.integration_amplitude
def test_amplitude_connection_test(amplitude_connection_config) -> None:
    get_connector(amplitude_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_amplitude
@pytest.mark.asyncio
async def test_amplitude_access_request_task(
    db,
    policy,
    amplitude_connection_config,
    amplitude_dataset_config,
    amplitude_identity_email,
) -> None:
    """Full access request based on the amplitude SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_amplitude_access_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": amplitude_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = amplitude_connection_config.get_saas_config().fides_key
    merged_graph = amplitude_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [amplitude_connection_config],
        {"email": amplitude_identity_email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:search_user"],
        min_size=1,
        keys=[
            "user_id",
            "amplitude_id",
            "last_device_id",
            "country",
            "last_seen"
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:user_activity"],
        min_size=1,
        keys=[
            "events",
            "userData",
            "metadata"
        ],
    )

    # verify we only returned data for our identity email
    assert v[f"{dataset_name}:search_user"][0]["user_id"] == amplitude_identity_email
    amplitude_id = v[f"{dataset_name}:search_user"][0]["amplitude_id"]


@pytest.mark.integration_saas
@pytest.mark.integration_amplitude
@pytest.mark.asyncio
async def test_amplitude_erasure_request_task(
    db,
    policy,
    erasure_policy_string_rewrite,
    amplitude_connection_config,
    amplitude_dataset_config,
    amplitude_erasure_identity_email,
    amplitude_create_erasure_data,
) -> None:
    """Full erasure request based on the amplitude SaaS config"""

    masking_strict = CONFIG.execution.masking_strict
    CONFIG.execution.masking_strict = True  # Allow Delete

    privacy_request = PrivacyRequest(
        id=f"test_amplitude_erasure_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": amplitude_erasure_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = amplitude_connection_config.get_saas_config().fides_key
    merged_graph = amplitude_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [amplitude_connection_config],
        {"email": amplitude_erasure_identity_email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:search_user"],
        min_size=1,
        keys=[
            "user_id",
            "amplitude_id",
            "last_device_id",
            "country",
            "last_seen"
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:user_activity"],
        min_size=1,
        keys=[
            "events",
            "userData",
            "metadata"
        ],
    )

    x = await graph_task.run_erasure(
        privacy_request,
        erasure_policy_string_rewrite,
        graph,
        [amplitude_connection_config],
        {"email": amplitude_erasure_identity_email},
        get_cached_data_for_erasures(privacy_request.id),
        db,
    )

    assert x == {
        f"{dataset_name}:search_user": 0,
        f"{dataset_name}:user_activity": 1,
    }

    amplitude_secrets = amplitude_connection_config.secrets
    base_url = f"https://{amplitude_secrets['domain']}"
    headers = {
        "Authorization": f"Basic {amplitude_secrets['api_key']}",
    }

    # user
    response = requests.get(
        url=f"{base_url}/api/2/usersearch",
        auth=auth,
        params={"email": amplitude_erasure_identity_email},
    )
    # Since user is deleted, it won't be available so response is 404
    assert response.status_code == 200

    CONFIG.execution.masking_strict = masking_strict

