from __future__ import annotations

import pytest
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from starlette.testclient import TestClient

from fides.api.api.v1.endpoints.privacy_experience_config_endpoints import (
    get_experience_config_or_error,
)
from fides.api.models.privacy_experience import (
    BannerEnabled,
    ComponentType,
    PrivacyExperience,
    PrivacyExperienceConfig,
    PrivacyExperienceConfigHistory,
    link_notices_to_experience_config,
)
from fides.api.models.privacy_notice import PrivacyNoticeRegion
from fides.common.api import scope_registry as scopes
from fides.common.api.v1.urn_registry import EXPERIENCE_CONFIG, V1_URL_PREFIX


class TestGetExperienceConfigList:
    @pytest.fixture(scope="function")
    def url(self) -> str:
        return V1_URL_PREFIX + EXPERIENCE_CONFIG

    def test_get_experience_config_unauthenticated(self, url, api_client):
        resp = api_client.get(url)
        assert resp.status_code == 401

    def test_get_experience_config_wrong_scope(
        self, url, api_client: TestClient, generate_auth_header
    ):
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_NOTICE_READ])
        resp = api_client.get(
            url,
            headers=auth_header,
        )
        assert resp.status_code == 403

    @pytest.mark.parametrize(
        "role,expected_status",
        [
            ("owner", HTTP_200_OK),
            ("contributor", HTTP_200_OK),
            ("viewer_and_approver", HTTP_200_OK),
            ("viewer", HTTP_200_OK),
            ("approver", HTTP_403_FORBIDDEN),
        ],
    )
    def test_get_experience_config_with_roles(
        self,
        role,
        expected_status,
        api_client: TestClient,
        url,
        generate_role_header,
    ) -> None:
        auth_header = generate_role_header(roles=[role])
        response = api_client.get(url, headers=auth_header)
        assert response.status_code == expected_status

    @pytest.mark.usefixtures(
        "privacy_experience_privacy_center", "privacy_experience_overlay"
    )
    def test_get_experience_config_list(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_privacy_center,
        experience_config_overlay,
    ) -> None:
        unescape_header = {"Unescape-Safestr": "true"}
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(url, headers={**auth_header, **unescape_header})
        assert response.status_code == 200
        resp = response.json()
        assert (
            resp["total"] == 4
        )  # Two default configs loaded on startup plus two here. TCF Experience is excluded.
        assert resp["page"] == 1
        assert resp["size"] == 50
        data = resp["items"]
        assert len(data) == 4

        first_config = data[0]
        assert first_config["id"] == experience_config_overlay.id
        assert (
            first_config["description"]
            == "On this page you can opt in and out of these data uses cases"
        )
        assert (
            first_config["banner_description"]
            == "You can accept, reject, or manage your preferences in detail."
        )
        assert first_config["banner_title"] == "Manage Your Consent"
        assert first_config["component"] == "overlay"
        assert first_config["banner_enabled"] == "enabled_where_required"
        assert first_config["disabled"] is False
        assert first_config["regions"] == ["us_ca"]
        assert first_config["version"] == 1.0
        assert first_config["created_at"] is not None
        assert first_config["updated_at"] is not None
        assert (
            first_config["experience_config_history_id"]
            == experience_config_overlay.experience_config_history_id
        )

        second_config = data[1]
        assert second_config["id"] == experience_config_privacy_center.id
        assert (
            second_config["description"] == "user's description "
        )  # Sanitized due to HtmlStr
        assert second_config["banner_description"] is None
        assert second_config["component"] == "privacy_center"
        assert second_config["banner_enabled"] is None
        assert second_config["disabled"] is True
        assert second_config["regions"] == ["us_co"]
        assert second_config["created_at"] is not None
        assert second_config["updated_at"] is not None
        assert second_config["version"] == 1.0
        assert (
            second_config["experience_config_history_id"]
            == experience_config_privacy_center.experience_config_history_id
        )

        third_config = data[2]
        assert third_config["id"] == "pri-097a-d00d-40b6-a08f-f8e50def-pri"
        assert third_config["is_default"] is True
        assert third_config["component"] == "privacy_center"
        assert third_config["regions"] == []
        assert third_config["version"] == 1.0
        assert third_config["created_at"] is not None
        assert third_config["updated_at"] is not None

        fourth_config = data[3]
        assert fourth_config["id"] == "pri-7ae3-f06b-4096-970f-0bbbdef-over"
        assert fourth_config["is_default"] is True
        assert fourth_config["disabled"] is False
        assert fourth_config["regions"] == []
        assert fourth_config["component"] == "overlay"

        response = api_client.get(
            url + "?component=tcf_overlay", headers={**auth_header, **unescape_header}
        )
        # Even if the TCF Overlay is requested it doesn't show up
        assert response.status_code == 200
        assert response.json()["items"] == []
        assert response.json()["total"] == 0

    @pytest.mark.usefixtures("enable_tcf")
    def test_get_tcf_experience_config(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        """TCF Experience Config is returned if TCF is enabled"""
        unescape_header = {"Unescape-Safestr": "true"}
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(url, headers={**auth_header, **unescape_header})
        assert response.status_code == 200
        resp = response.json()
        assert (
            resp["total"] == 3
        )  # All three default configs loaded on startup including TCF Experience
        assert resp["page"] == 1
        assert resp["size"] == 50
        data = resp["items"]
        assert len(data) == 3

        first_config = data[0]
        assert first_config["id"] == "a4974670-abad-471f-9084-2cb-tcf-over"
        assert first_config["is_default"] is True
        assert first_config["component"] == "tcf_overlay"
        assert first_config["regions"] == []
        assert first_config["version"] == 1.0
        assert first_config["created_at"] is not None
        assert first_config["updated_at"] is not None

        second_config = data[1]
        assert second_config["id"] == "pri-097a-d00d-40b6-a08f-f8e50def-pri"
        assert second_config["is_default"] is True
        assert second_config["component"] == "privacy_center"
        assert second_config["regions"] == []
        assert second_config["version"] == 1.0
        assert second_config["created_at"] is not None
        assert second_config["updated_at"] is not None

        third_config = data[2]
        assert third_config["id"] == "pri-7ae3-f06b-4096-970f-0bbbdef-over"
        assert third_config["is_default"] is True
        assert third_config["disabled"] is False
        assert third_config["regions"] == []
        assert third_config["component"] == "overlay"

    @pytest.mark.usefixtures(
        "privacy_experience_privacy_center",
        "privacy_experience_overlay",
        "experience_config_overlay",
    )
    def test_get_experience_config_list_no_unescape_header(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_privacy_center,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(url, headers=auth_header)
        assert response.status_code == 200
        resp = response.json()["items"]

        second_config = resp[1]
        assert second_config["id"] == experience_config_privacy_center.id
        assert (
            second_config["description"] == "user's description &lt;script /&gt;"
        )  # Still escaped
        assert second_config["banner_description"] is None

    @pytest.mark.usefixtures(
        "privacy_experience_overlay",
        "privacy_experience_privacy_center",
        "experience_config_privacy_center",
    )
    def test_get_experience_config_show_disabled_false_filter(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_overlay,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(
            url + "?show_disabled=False",
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()
        assert resp["total"] == 3
        assert resp["page"] == 1
        assert resp["size"] == 50
        data = resp["items"]
        assert len(data) == 3

        config = data[0]
        assert config["id"] == experience_config_overlay.id
        assert config["component"] == "overlay"
        assert config["disabled"] is False
        assert config["regions"] == ["us_ca"]
        assert config["version"] == 1.0
        assert config["created_at"] is not None
        assert config["updated_at"] is not None
        assert (
            config["experience_config_history_id"]
            == experience_config_overlay.experience_config_history_id
        )

        third_config = data[1]
        assert third_config["id"] == "pri-097a-d00d-40b6-a08f-f8e50def-pri"
        assert third_config["is_default"] is True
        assert third_config["component"] == "privacy_center"
        assert third_config["disabled"] is False
        assert third_config["version"] == 1.0
        assert third_config["created_at"] is not None
        assert third_config["updated_at"] is not None

        fourth_config = data[2]
        assert fourth_config["id"] == "pri-7ae3-f06b-4096-970f-0bbbdef-over"
        assert fourth_config["is_default"] is True
        assert fourth_config["disabled"] is False
        assert fourth_config["regions"] == []
        assert fourth_config["component"] == "overlay"

    @pytest.mark.usefixtures(
        "privacy_experience_overlay",
        "experience_config_privacy_center",
    )
    def test_get_experience_config_region_filter(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_overlay,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(
            url + "?region=us_ca",
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()
        assert resp["total"] == 1
        assert resp["page"] == 1
        assert resp["size"] == 50
        data = resp["items"]
        assert len(data) == 1

        first_config = data[0]
        assert first_config["id"] == experience_config_overlay.id
        assert first_config["regions"] == ["us_ca"]
        assert first_config["version"] == 1.0
        assert first_config["created_at"] is not None
        assert first_config["updated_at"] is not None
        assert (
            first_config["experience_config_history_id"]
            == experience_config_overlay.experience_config_history_id
        )

    def test_get_experience_config_component_filter(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_overlay,
        experience_config_privacy_center,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(
            url + "?component=overlay",
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()
        assert resp["total"] == 2
        assert resp["page"] == 1
        assert resp["size"] == 50
        data = resp["items"]
        assert len(data) == 2

        assert data[0]["id"] == experience_config_overlay.id
        assert data[1]["id"] == "pri-7ae3-f06b-4096-970f-0bbbdef-over"

        response = api_client.get(
            url + "?component=privacy_center",
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()
        assert resp["total"] == 2
        assert resp["page"] == 1
        assert resp["size"] == 50
        data = resp["items"]
        assert len(data) == 2

        assert data[0]["id"] == experience_config_privacy_center.id
        assert data[1]["id"] == "pri-097a-d00d-40b6-a08f-f8e50def-pri"


class TestCreateExperienceConfig:
    @pytest.fixture(scope="function")
    def url(self) -> str:
        return V1_URL_PREFIX + EXPERIENCE_CONFIG

    @pytest.fixture(scope="function")
    def overlay_experience_request_body(self) -> dict:
        return {
            "acknowledge_button_label": "Confirm",
            "banner_description": "You can accept, reject, or manage your preferences in detail.",
            "banner_enabled": "enabled_where_required",
            "banner_title": "Manage Your Consent",
            "component": "overlay",
            "description": "We care about your privacy. Opt in and opt out of the data use cases below.",
            "accept_button_label": "Accept all",
            "disabled": False,
            "privacy_preferences_link_label": "Manage preferences",
            "privacy_policy_link_label": "View our privacy policy",
            "privacy_policy_url": "http://example.com/privacy",
            "reject_button_label": "Reject all",
            "regions": [],
            "save_button_label": "Save",
            "title": "Control your privacy",
        }

    def test_create_experience_config_unauthenticated(self, url, api_client):
        resp = api_client.post(url)
        assert resp.status_code == 401

    def test_create_experience_config_wrong_scope(
        self, url, api_client: TestClient, generate_auth_header
    ):
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        resp = api_client.post(
            url,
            headers=auth_header,
        )
        assert resp.status_code == 403

    @pytest.mark.parametrize(
        "role,expected_status",
        [
            ("owner", HTTP_201_CREATED),
            ("contributor", HTTP_201_CREATED),
            ("viewer_and_approver", HTTP_403_FORBIDDEN),
            ("viewer", HTTP_403_FORBIDDEN),
            ("approver", HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_experience_config_with_roles(
        self,
        role,
        expected_status,
        api_client: TestClient,
        url,
        generate_role_header,
        overlay_experience_request_body,
    ) -> None:
        auth_header = generate_role_header(roles=[role])
        response = api_client.post(
            url, json=overlay_experience_request_body, headers=auth_header
        )
        assert response.status_code == expected_status

    def test_create_overlay_config_missing_details(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Accept",
                "description": "We care about your privacy",
                "component": "overlay",
                "regions": ["it"],
                "reject_button_label": "Reject",
                "save_button_label": "Save",
                "title": "Manage your privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "The following additional fields are required when defining an overlay: acknowledge_button_label, banner_enabled, and privacy_preferences_link_label."
        )

    def test_create_privacy_center_config_missing_details(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Accept",
                "description": "We care about your privacy",
                "component": "privacy_center",
                "regions": ["it"],
                "save_button_label": "Save",
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "field required"

    def test_create_experience_duplicate_regions(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Accept all",
                "description": "We care about your privacy",
                "component": "privacy_center",
                "reject_button_label": "Reject all",
                "save_button_label": "Save",
                "title": "Control your privacy",
                "regions": ["it", "it"],
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Duplicate regions found."

    def test_create_another_default_experience_config(
        self, api_client: TestClient, url, generate_auth_header, db
    ) -> None:
        """We have defaults loaded in at startup so don't allow other defaults to be created here"""
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Yes",
                "banner_enabled": "always_disabled",
                "component": "privacy_center",
                "description": "We take your privacy seriously",
                "is_default": True,
                "privacy_policy_link_label": "Manage your privacy",
                "privacy_policy_url": "http://example.com/privacy",
                "reject_button_label": "No",
                "save_button_label": "Save",
                "title": "Manage your privacy",
            },
            headers=auth_header,
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"]
            == "Cannot set as the default. Only one default privacy_center config can be in the system."
        )

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "thisisnotaurl",
            "javascript:alert('XSS: domain scope: '+document.domain)",
        ],
    )
    def test_create_experience_config_with_invalid_policy_url(
        self, api_client: TestClient, url, generate_auth_header, db, invalid_url
    ) -> None:
        """
        Verify that an invalid Privacy Policy URL returns a 422.
        """
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Yes",
                "banner_enabled": "always_disabled",
                "component": "privacy_center",
                "description": "We take your company's privacy seriously",
                "privacy_policy_link_label": "Manage your privacy",
                "privacy_policy_url": invalid_url,
                "reject_button_label": "No",
                "save_button_label": "Save",
                "title": "Manage your privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 422

    def test_create_experience_config_with_no_regions(
        self, api_client: TestClient, url, generate_auth_header, db
    ) -> None:
        """Experience config can be defined without any regions specified. This is handy for defining default experiences

        No privacy experiences are affected here.  But ExperienceConfig and ExperienceConfigHistory records are created.
        """
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Yes",
                "banner_enabled": "always_disabled",
                "component": "privacy_center",
                "description": "We take your company's privacy seriously",
                "privacy_policy_link_label": "Manage your privacy",
                "privacy_policy_url": "http://example.com/privacy",
                "reject_button_label": "No",
                "save_button_label": "Save",
                "title": "Manage your privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 201
        resp = response.json()["experience_config"]
        assert resp["accept_button_label"] == "Yes"
        assert resp["banner_enabled"] == "always_disabled"
        assert resp["component"] == "privacy_center"
        assert (
            resp["description"] == "We take your company's privacy seriously"
        )  # Returned in the response, unescaped, for display
        assert resp["privacy_policy_link_label"] == "Manage your privacy"
        assert resp["privacy_policy_url"] == "http://example.com/privacy"
        assert resp["regions"] == []
        assert resp["reject_button_label"] == "No"
        assert resp["save_button_label"] == "Save"
        assert resp["title"] == "Manage your privacy"
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["version"] == 1.0

        experience_config = get_experience_config_or_error(db, resp["id"])
        assert experience_config.component == ComponentType.privacy_center
        assert experience_config.privacy_policy_link_label == "Manage your privacy"
        assert experience_config.experiences.all() == []
        assert experience_config.histories.count() == 1
        assert (
            experience_config.description
            == "We take your company&#x27;s privacy seriously"
        )  # Saved in the db escaped
        history = experience_config.histories[0]
        assert history.version == 1.0
        assert history.component == ComponentType.privacy_center
        assert history.privacy_policy_link_label == "Manage your privacy"
        assert history.experience_config_id == experience_config.id

        assert response.json()["linked_regions"] == []
        assert response.json()["unlinked_regions"] == []

        history.delete(db)
        experience_config.delete(db)

    def test_create_experience_config_with_empty_regions(
        self, api_client: TestClient, url, generate_auth_header, db
    ) -> None:
        """Experience config can be defined without any regions specified. This is handy for defining default experiences

        No privacy experiences are affected here.  But ExperienceConfig and ExperienceConfigHistory records are created.
        """
        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Yes",
                "banner_enabled": "always_disabled",
                "component": "privacy_center",
                "description": "We take your privacy seriously",
                "privacy_policy_link_label": "Manage your privacy",
                "privacy_policy_url": "http://example.com/privacy",
                "regions": [],
                "reject_button_label": "No",
                "save_button_label": "Save",
                "title": "Manage your privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 201
        resp = response.json()["experience_config"]
        assert resp["accept_button_label"] == "Yes"
        assert resp["banner_enabled"] == "always_disabled"
        assert resp["component"] == "privacy_center"
        assert resp["description"] == "We take your privacy seriously"
        assert resp["privacy_policy_link_label"] == "Manage your privacy"
        assert resp["privacy_policy_url"] == "http://example.com/privacy"
        assert resp["regions"] == []
        assert resp["reject_button_label"] == "No"
        assert resp["save_button_label"] == "Save"
        assert resp["title"] == "Manage your privacy"
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["version"] == 1.0

        experience_config = get_experience_config_or_error(db, resp["id"])
        assert experience_config.component == ComponentType.privacy_center
        assert experience_config.privacy_policy_link_label == "Manage your privacy"
        assert experience_config.experiences.all() == []
        assert experience_config.histories.count() == 1
        history = experience_config.histories[0]
        assert history.version == 1.0
        assert history.component == ComponentType.privacy_center
        assert history.privacy_policy_link_label == "Manage your privacy"
        assert history.experience_config_id == experience_config.id

        assert response.json()["linked_regions"] == []
        assert response.json()["unlinked_regions"] == []

        history.delete(db)
        experience_config.delete(db)

    def test_create_experience_config_no_existing_experiences(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
    ) -> None:
        """
        Specifying a NY region to be used with the new ExperienceConfig will
        cause a NY PrivacyExperience to be created behind the scenes if one doesn't exist.
        """

        assert (
            PrivacyExperience.get_experience_by_region_and_component(
                db, PrivacyNoticeRegion.us_ny, ComponentType.overlay
            )
            is None
        )

        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Accept all",
                "acknowledge_button_label": "Confirm",
                "banner_enabled": "enabled_where_required",
                "component": "overlay",
                "description": "We care about your privacy. Opt in and opt out of the data use cases below.",
                "privacy_preferences_link_label": "Control your privacy",
                "privacy_policy_link_label": "Control your privacy",
                "privacy_policy_url": "http://example.com/privacy",
                "regions": ["us_ny"],
                "reject_button_label": "Reject all",
                "save_button_label": "Save",
                "title": "Control your privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 201
        resp = response.json()["experience_config"]
        assert resp["accept_button_label"] == "Accept all"
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["component"] == "overlay"
        assert resp["created_at"] is not None
        assert (
            resp["description"]
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert resp["privacy_preferences_link_label"] == "Control your privacy"
        assert resp["privacy_policy_link_label"] == "Control your privacy"
        assert resp["privacy_policy_url"] == "http://example.com/privacy"
        assert resp["regions"] == ["us_ny"]
        assert resp["reject_button_label"] == "Reject all"
        assert resp["save_button_label"] == "Save"
        assert resp["title"] == "Control your privacy"
        assert resp["version"] == 1.0
        assert resp["updated_at"] is not None

        # Created Experience Config
        experience_config = get_experience_config_or_error(db, resp["id"])
        assert experience_config.accept_button_label == "Accept all"
        assert experience_config.acknowledge_button_label == "Confirm"
        assert experience_config.banner_enabled == BannerEnabled.enabled_where_required
        assert experience_config.component == ComponentType.overlay
        assert (
            experience_config.description
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert (
            experience_config.privacy_preferences_link_label == "Control your privacy"
        )
        assert experience_config.privacy_policy_link_label == "Control your privacy"
        assert experience_config.privacy_policy_url == "http://example.com/privacy"
        assert experience_config.regions == [PrivacyNoticeRegion.us_ny]
        assert experience_config.reject_button_label == "Reject all"
        assert experience_config.save_button_label == "Save"
        assert experience_config.title == "Control your privacy"

        assert experience_config.created_at is not None
        assert experience_config.updated_at is not None
        assert experience_config.histories.count() == 1

        # Created Experience Config History
        experience_config_history = experience_config.histories[0]
        assert experience_config_history.version == 1.0

        assert experience_config_history.accept_button_label == "Accept all"
        assert experience_config_history.acknowledge_button_label == "Confirm"
        assert (
            experience_config_history.banner_enabled
            == BannerEnabled.enabled_where_required
        )
        assert experience_config_history.component == ComponentType.overlay
        assert (
            experience_config_history.description
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert (
            experience_config_history.privacy_preferences_link_label
            == "Control your privacy"
        )
        assert (
            experience_config_history.privacy_policy_link_label
            == "Control your privacy"
        )
        assert (
            experience_config_history.privacy_policy_url == "http://example.com/privacy"
        )
        assert experience_config_history.reject_button_label == "Reject all"
        assert experience_config_history.save_button_label == "Save"
        assert experience_config_history.title == "Control your privacy"

        assert experience_config_history.created_at is not None
        assert experience_config_history.updated_at is not None
        assert experience_config_history.experience_config_id == experience_config.id

        # Created Privacy Experience
        assert experience_config.experiences.count() == 1
        experience = experience_config.experiences[0]
        assert experience.region == PrivacyNoticeRegion.us_ny
        assert experience.component == ComponentType.overlay
        assert experience.experience_config_id == experience_config.id

        experience.delete(db)
        experience_config_history.delete(db)
        experience_config.delete(db)

        assert response.json()["linked_regions"] == ["us_ny"]
        assert response.json()["unlinked_regions"] == []

    def test_create_experience_config_existing_experiences(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
    ) -> None:
        """
        Specifying a TX region to be used with the new ExperienceConfig can
        cause an existing TX PrivacyExperience to be linked to the current ExperienceConfig
        """

        privacy_experience = PrivacyExperience.create(
            db,
            data={
                "component": ComponentType.overlay,
                "region": PrivacyNoticeRegion.us_tx,
            },
        )

        assert privacy_experience.experience_config_id is None

        auth_header = generate_auth_header(
            scopes=[scopes.PRIVACY_EXPERIENCE_CREATE, scopes.PRIVACY_EXPERIENCE_UPDATE]
        )
        response = api_client.post(
            url,
            json={
                "accept_button_label": "Accept all",
                "acknowledge_button_label": "Confirm",
                "banner_enabled": "enabled_where_required",
                "component": "overlay",
                "description": "We care about your privacy. Opt in and opt out of the data use cases below.",
                "privacy_preferences_link_label": "Control your privacy",
                "privacy_policy_link_label": "Control your privacy",
                "privacy_policy_url": "http://example.com/privacy",
                "regions": ["us_tx"],
                "reject_button_label": "Reject all",
                "save_button_label": "Save",
                "title": "Control your privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 201
        resp = response.json()["experience_config"]
        assert resp["accept_button_label"] == "Accept all"
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["component"] == "overlay"
        assert resp["created_at"] is not None
        assert (
            resp["description"]
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert resp["privacy_preferences_link_label"] == "Control your privacy"
        assert resp["privacy_policy_link_label"] == "Control your privacy"
        assert resp["privacy_policy_url"] == "http://example.com/privacy"
        assert resp["regions"] == ["us_tx"]
        assert resp["reject_button_label"] == "Reject all"
        assert resp["save_button_label"] == "Save"
        assert resp["title"] == "Control your privacy"
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["version"] == 1.0

        # Created Experience Config
        experience_config = get_experience_config_or_error(db, resp["id"])
        assert experience_config.histories.count() == 1

        # Created Experience Config History
        experience_config_history = experience_config.histories[0]
        assert experience_config_history.version == 1.0
        assert experience_config_history.component == ComponentType.overlay
        assert (
            experience_config_history.banner_enabled
            == BannerEnabled.enabled_where_required
        )
        assert experience_config_history.experience_config_id == experience_config.id

        # Updated Privacy Experience - TX Privacy Experience automatically linked
        assert experience_config.experiences.count() == 1
        experience = experience_config.experiences[0]
        db.refresh(experience)
        assert (
            experience == privacy_experience
        )  # Linked experience is the same Texas experience from above
        assert experience.region == PrivacyNoticeRegion.us_tx
        assert experience.component == ComponentType.overlay
        assert experience.experience_config_id == experience_config.id

        assert response.json()["linked_regions"] == ["us_tx"]
        assert response.json()["unlinked_regions"] == []

        experience.delete(db)
        experience_config_history.delete(db)
        experience_config.delete(db)


class TestGetExperienceConfigDetail:
    @pytest.fixture(scope="function")
    def url(self, experience_config_overlay) -> str:
        return V1_URL_PREFIX + EXPERIENCE_CONFIG + f"/{experience_config_overlay.id}"

    def test_get_experience_config_detail_unauthenticated(self, url, api_client):
        resp = api_client.get(url)
        assert resp.status_code == 401

    def test_get_experience_config_detail_wrong_scope(
        self, url, api_client: TestClient, generate_auth_header
    ):
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_NOTICE_READ])
        resp = api_client.get(
            url,
            headers=auth_header,
        )
        assert resp.status_code == 403

    @pytest.mark.parametrize(
        "role,expected_status",
        [
            ("owner", HTTP_200_OK),
            ("contributor", HTTP_200_OK),
            ("viewer_and_approver", HTTP_200_OK),
            ("viewer", HTTP_200_OK),
            ("approver", HTTP_403_FORBIDDEN),
        ],
    )
    def test_get_experience_config_detail_with_roles(
        self,
        role,
        expected_status,
        api_client: TestClient,
        url,
        generate_role_header,
    ) -> None:
        auth_header = generate_role_header(roles=[role])
        response = api_client.get(url, headers=auth_header)
        assert response.status_code == expected_status

    def test_get_bad_experience_config_detail(
        self,
        api_client: TestClient,
        generate_auth_header,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        url = V1_URL_PREFIX + EXPERIENCE_CONFIG + "/bad_id"

        response = api_client.get(
            url,
            headers=auth_header,
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "No Privacy Experience Config found for id 'bad_id'."
        )

    @pytest.mark.usefixtures(
        "privacy_experience_overlay",
    )
    def test_get_experience_config_detail(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_overlay,
        privacy_notice,
        db,
    ) -> None:
        link_notices_to_experience_config(
            db, [privacy_notice.notice_key], experience_config_overlay
        )

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(
            url,
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()

        assert resp["id"] == experience_config_overlay.id
        assert resp["component"] == "overlay"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["allow_language_selection"] is False
        assert not resp["dismissable"]

        assert resp["regions"] == ["us_ca"]
        assert resp["version"] == 1.0
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        translations = resp["translations"]
        assert len(translations) == 1
        translation = translations[0]

        assert translation["language"] == "en_us"
        assert translation["title"] == "Manage your consent"
        assert translation["acknowledge_button_label"] == "Confirm"
        assert (
            translation["banner_description"]
            == "You can accept, reject, or manage your preferences in detail."
        )
        assert translation["banner_title"] == "Manage Your Consent"
        assert translation["is_default"] is False
        assert translation["privacy_preferences_link_label"] == "Manage preferences"
        assert translation["accept_button_label"] == "Accept all"
        assert translation["reject_button_label"] == "Reject all"
        assert translation["save_button_label"] == "Save"
        assert (
            translation["description"]
            == "On this page you can opt in and out of these data uses cases"
        )
        assert translation["experience_config_history_id"] is not None
        assert (
            translation["experience_config_history_id"]
            == experience_config_overlay.translations[0].experience_config_history.id
        )
        assert (
            translation["privacy_policy_link_label"]
            == "View our company&#x27;s privacy policy"
        )  # Escaped without request header

        assert len(resp["privacy_notices"]) == 1
        privacy_notice_response = resp["privacy_notices"][0]
        assert privacy_notice_response["name"] == privacy_notice.name
        assert privacy_notice_response["notice_key"] == privacy_notice.notice_key
        assert privacy_notice_response["consent_mechanism"] == "opt_in"
        translations = privacy_notice_response["translations"]
        assert len(translations) == 1
        assert translations[0]["language"] == "en_us"
        assert translations[0]["privacy_notice_history_id"] is not None
        assert (
            translations[0]["privacy_notice_history_id"]
            == privacy_notice.translations[0].privacy_notice_history.id
        )

    @pytest.mark.usefixtures(
        "privacy_experience_overlay",
    )
    def test_get_experience_config_detail_with_unescape_header(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        experience_config_overlay,
    ) -> None:
        unescape_header = {"Unescape-Safestr": "true"}
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        response = api_client.get(url, headers={**auth_header, **unescape_header})
        assert response.status_code == 200
        resp = response.json()

        assert resp["id"] == experience_config_overlay.id
        assert resp["component"] == "overlay"
        assert (
            resp["privacy_policy_link_label"] == "View our company's privacy policy"
        )  # Unescaped with request header


class TestUpdateExperienceConfig:
    @pytest.fixture(scope="function")
    def url(self, overlay_experience_config) -> str:
        return V1_URL_PREFIX + EXPERIENCE_CONFIG + f"/{overlay_experience_config.id}"

    @pytest.fixture(scope="function")
    def overlay_experience_config(self, db) -> PrivacyExperienceConfig:
        exp = PrivacyExperienceConfig.create(
            db=db,
            data={
                "accept_button_label": "Accept all",
                "acknowledge_button_label": "Confirm",
                "banner_enabled": "enabled_where_required",
                "component": "overlay",
                "description": "We care about your privacy. Opt in and opt out of the data use cases below.",
                "disabled": False,
                "privacy_preferences_link_label": "Manage preferences",
                "privacy_policy_link_label": "View our privacy policy",
                "privacy_policy_url": "http://example.com/privacy",
                "reject_button_label": "Reject all",
                "save_button_label": "Save",
                "title": "Control your privacy",
            },
        )
        yield exp
        for history in exp.histories:
            history.delete(db)
        exp.delete(db)

    def test_update_experience_config_unauthenticated(self, url, api_client):
        resp = api_client.patch(url, json={"disabled": True})
        assert resp.status_code == 401

    def test_update_experience_config_wrong_scope(
        self, url, api_client: TestClient, generate_auth_header
    ):
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_READ])
        resp = api_client.patch(
            url,
            headers=auth_header,
        )
        assert resp.status_code == 403

    @pytest.mark.parametrize(
        "role,expected_status",
        [
            ("owner", HTTP_200_OK),
            ("contributor", HTTP_200_OK),
            ("viewer_and_approver", HTTP_403_FORBIDDEN),
            ("viewer", HTTP_403_FORBIDDEN),
            ("approver", HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_experience_config_with_roles(
        self,
        role,
        expected_status,
        api_client: TestClient,
        url,
        generate_role_header,
    ) -> None:
        auth_header = generate_role_header(roles=[role])
        response = api_client.patch(
            url, json={"disabled": True, "regions": []}, headers=auth_header
        )
        assert response.status_code == expected_status

    def test_update_experience_config_duplicate_regions(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        """Failing if duplicate regions in request to avoid unexpected behavior"""
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "title": "We care about your privacy",
                "regions": ["us_ca", "us_ca"],
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Duplicate regions found."

    def test_update_bad_experience_config(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        """Nonexistent experience config id"""
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            V1_URL_PREFIX + EXPERIENCE_CONFIG + "/bad_experience_id",
            json={
                "title": "We care about your privacy",
                "regions": ["us_ca"],
            },
            headers=auth_header,
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "No Privacy Experience Config found for id 'bad_experience_id'."
        )

    def test_update_overlay_experience_config_missing_details(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={"title": None},
            headers=auth_header,
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "none is not an allowed value"

    def test_update_overlay_experience_config_missing_overlay_specific_fields(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])

        response = api_client.patch(
            url,
            json={
                "privacy_preferences_link_label": "",
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "The following additional fields are required when defining an overlay: acknowledge_button_label, banner_enabled, and privacy_preferences_link_label."
        )

    def test_update_as_default(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        overlay_experience_config,
    ):
        """We already have a default overlay added to the system on startup, so we don't
        want to update this separate overlay to be a default"""
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "is_default": True,
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert (
            response.json()["detail"]
            == "Cannot set as the default. Only one default overlay config can be in the system."
        )

    def test_update_experience_config_with_fields_that_should_be_escaped(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        overlay_experience_config,
        db,
    ) -> None:
        """Failing if duplicate regions in request to avoid unexpected behavior"""
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "title": "We care about you and your family's privacy",
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        assert (
            response.json()["experience_config"]["title"]
            == "We care about you and your family's privacy"
        )  # Unescaped in response
        db.refresh(overlay_experience_config)
        assert (
            overlay_experience_config.title
            == "We care about you and your family&#x27;s privacy"
        )  # But stored escaped

    def test_attempt_to_update_component_type(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ) -> None:
        """Component type can't be edited once created"""
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])

        response = api_client.patch(
            url,
            json={
                "component": "privacy_center",
            },
            headers=auth_header,
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "extra fields not permitted"

    def test_update_experience_config_while_ignoring_regions(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        experience_config_overlay,
        privacy_experience_overlay,
    ) -> None:
        """We need to currently support editing experience configs without the regions.  If "regions" is None,
        I don't edit regions at all. If "regions" are an empty list, they are all removed.
        """
        assert experience_config_overlay.disabled is False
        assert experience_config_overlay.regions == [PrivacyNoticeRegion.us_ca]

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            V1_URL_PREFIX + EXPERIENCE_CONFIG + f"/{experience_config_overlay.id}",
            json={
                "disabled": True,
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()["experience_config"]
        assert resp["disabled"] is True
        assert resp["regions"] == ["us_ca"]  # Main thing, regions weren't touched!
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["disabled"] is True
        assert resp["version"] == 2.0

        experience_config = get_experience_config_or_error(db, resp["id"])
        assert experience_config.experiences.all() == [privacy_experience_overlay]
        assert experience_config.histories.count() == 2
        history = experience_config.histories.order_by(
            PrivacyExperienceConfigHistory.created_at
        )[0]
        assert history.version == 1.0
        assert history.component == ComponentType.overlay
        assert history.banner_enabled == BannerEnabled.enabled_where_required
        assert history.experience_config_id == experience_config.id
        assert history.disabled is False

        history = experience_config.histories.order_by(
            PrivacyExperienceConfigHistory.created_at
        )[1]
        assert history.version == 2.0
        assert history.disabled is True

        assert response.json()["linked_regions"] == []
        assert response.json()["unlinked_regions"] == []

        privacy_experience_overlay.delete(db)

        for history in experience_config.histories:
            history.delete(db)
        experience_config.delete(db)

    def test_update_experience_config_with_no_regions(
        self, api_client: TestClient, url, generate_auth_header, db
    ) -> None:
        """Test scenario where experience config has no regions and we make updates without any regions being
        involved.  Specifically disabling the ExperienceConfig
        """
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "disabled": True,
                "regions": [],
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()["experience_config"]
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["component"] == "overlay"
        assert resp["title"] == "Control your privacy"
        assert (
            resp["description"]
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert resp["accept_button_label"] == "Accept all"
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["reject_button_label"] == "Reject all"
        assert resp["regions"] == []
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["disabled"] is True
        assert resp["version"] == 2.0

        experience_config = get_experience_config_or_error(db, resp["id"])
        assert experience_config.experiences.all() == []
        assert experience_config.histories.count() == 2
        history = experience_config.histories.order_by(
            PrivacyExperienceConfigHistory.created_at
        )[0]
        assert history.version == 1.0
        assert history.component == ComponentType.overlay
        assert history.banner_enabled == BannerEnabled.enabled_where_required
        assert history.experience_config_id == experience_config.id
        assert history.disabled is False

        history = experience_config.histories.order_by(
            PrivacyExperienceConfigHistory.created_at
        )[1]
        assert history.version == 2.0
        assert history.disabled is True

        assert response.json()["linked_regions"] == []
        assert response.json()["unlinked_regions"] == []

        for history in experience_config.histories:
            history.delete(db)
        experience_config.delete(db)

    def test_update_experience_config_no_existing_experiences(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        overlay_experience_config,
    ) -> None:
        """
        This action is updating an existing ExperienceConfig to add NY.  NY does not have a PrivacyExperience
        yet, so one will be created for it.
        """

        assert (
            PrivacyExperience.get_experience_by_region_and_component(
                db, PrivacyNoticeRegion.us_ny, ComponentType.overlay
            )
            is None
        )

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={"regions": ["us_ny"]},
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()["experience_config"]
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["component"] == "overlay"
        assert resp["title"] == "Control your privacy"
        assert (
            resp["description"]
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert resp["accept_button_label"] == "Accept all"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["reject_button_label"] == "Reject all"
        assert resp["regions"] == ["us_ny"]
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["version"] == 1.0

        # ExperienceConfig specifically wasn't updated, as this change is only changing which regions link here as FK
        db.refresh(overlay_experience_config)
        assert overlay_experience_config.id == resp["id"]
        assert overlay_experience_config.histories.count() == 1

        # Existing Experience Config History
        experience_config_history = overlay_experience_config.histories[0]
        assert experience_config_history.version == 1.0
        assert experience_config_history.component == ComponentType.overlay
        assert (
            experience_config_history.experience_config_id
            == overlay_experience_config.id
        )

        # Created Privacy Experience
        assert overlay_experience_config.experiences.count() == 1
        experience = overlay_experience_config.experiences[0]
        assert experience.region == PrivacyNoticeRegion.us_ny
        assert experience.component == ComponentType.overlay
        assert experience.experience_config_id == overlay_experience_config.id

        experience.delete(db)

        assert response.json()["linked_regions"] == ["us_ny"]
        assert response.json()["unlinked_regions"] == []

    def test_update_experience_config_regions_to_overlap_on_existing_experiences(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        overlay_experience_config,
    ) -> None:
        """
        Existing ExperienceConfig is updated to add TX.  A Texas Privacy Experience already exists.

        This should cause the existing Texas PrivacyExperience to be given a FK to the existing ExperienceConfig record
        """

        privacy_experience = PrivacyExperience.create(
            db,
            data={
                "component": ComponentType.overlay,
                "region": PrivacyNoticeRegion.us_tx,
            },
        )

        assert privacy_experience.experience_config_id is None

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "regions": ["us_tx"],
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()["experience_config"]
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["component"] == "overlay"
        assert resp["title"] == "Control your privacy"
        assert (
            resp["description"]
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert resp["accept_button_label"] == "Accept all"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["reject_button_label"] == "Reject all"
        assert resp["regions"] == ["us_tx"]
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert (
            resp["version"] == 1.0
        ), "Version not bumped because config didn't change on ExperienceConfig"

        db.refresh(overlay_experience_config)
        # Existing Experience Config History - no new version needed to be created
        assert overlay_experience_config.histories.count() == 1
        experience_config_history = overlay_experience_config.histories[0]
        assert experience_config_history.version == 1.0
        assert experience_config_history.component == ComponentType.overlay
        assert (
            experience_config_history.banner_enabled
            == BannerEnabled.enabled_where_required
        )
        assert (
            experience_config_history.experience_config_id
            == overlay_experience_config.id
        )

        # Updated Privacy Experience - TX Privacy Experience automatically linked
        assert overlay_experience_config.experiences.count() == 1
        experience = overlay_experience_config.experiences[0]
        db.refresh(experience)
        assert (
            experience == privacy_experience
        )  # Linked experience is the same Texas experience from above
        assert experience.region == PrivacyNoticeRegion.us_tx
        assert experience.component == ComponentType.overlay
        assert experience.experience_config_id == overlay_experience_config.id

        assert response.json()["linked_regions"] == ["us_tx"]
        assert response.json()["unlinked_regions"] == []

        experience.delete(db)

    def test_update_experience_config_experience_also_updated(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        overlay_experience_config,
    ) -> None:
        """
        Verify that if the ExperienceConfig is updated, some of those updates are passed onto the PrivacyExperience record.

        Existing ExperienceConfig is updated to add TX.  A Texas Privacy Experience already exists.
        We are updating the existing ExperienceConfig simultaneously. So the TX PrivacyExperience will
        be linked to the ExperienceConfig and also have select attributes from ExperienceConfig propagated back
        """

        privacy_experience = PrivacyExperience.create(
            db,
            data={
                "component": ComponentType.overlay,
                "region": PrivacyNoticeRegion.us_tx,
            },
        )

        assert privacy_experience.experience_config_id is None

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={"regions": ["us_tx"], "disabled": True},
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()["experience_config"]
        assert resp["acknowledge_button_label"] == "Confirm"
        assert resp["component"] == "overlay"
        assert resp["title"] == "Control your privacy"
        assert (
            resp["description"]
            == "We care about your privacy. Opt in and opt out of the data use cases below."
        )
        assert resp["accept_button_label"] == "Accept all"
        assert resp["banner_enabled"] == "enabled_where_required"
        assert resp["reject_button_label"] == "Reject all"
        assert resp["regions"] == ["us_tx"]
        assert resp["created_at"] is not None
        assert resp["updated_at"] is not None
        assert resp["disabled"] is True
        assert (
            resp["version"] == 2.0
        ), "Version bumped because we've disabled ExperienceConfig"

        db.refresh(overlay_experience_config)
        # ExperienceConfig was disabled - this is a change, so another historical record is created
        assert overlay_experience_config.histories.count() == 2
        experience_config_history = overlay_experience_config.histories.order_by(
            PrivacyExperienceConfigHistory.created_at
        )[1]
        assert experience_config_history.version == 2.0
        assert experience_config_history.disabled
        assert experience_config_history.component == ComponentType.overlay
        assert (
            experience_config_history.banner_enabled
            == BannerEnabled.enabled_where_required
        )
        assert (
            experience_config_history.experience_config_id
            == overlay_experience_config.id
        )

        # Updated Privacy Experience - TX Privacy Experience automatically linked
        assert overlay_experience_config.experiences.count() == 1
        experience = overlay_experience_config.experiences[0]
        db.refresh(experience)
        assert (
            experience == privacy_experience
        )  # Linked experience is the same Texas experience from above
        assert experience.region == PrivacyNoticeRegion.us_tx
        assert experience.component == ComponentType.overlay
        assert experience.experience_config_id == overlay_experience_config.id

        assert response.json()["linked_regions"] == ["us_tx"]
        assert response.json()["unlinked_regions"] == []

        experience.delete(db)

    def test_update_experience_config_to_remove_region(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        overlay_experience_config,
    ) -> None:
        """
        Update the ExperienceConfig to remove a region. Verify this unlinks the region.
        """

        privacy_experience = PrivacyExperience.create(
            db,
            data={
                "component": ComponentType.overlay,
                "region": PrivacyNoticeRegion.us_tx,
                "experience_config_id": overlay_experience_config.id,
            },
        )

        assert privacy_experience.experience_config_id == overlay_experience_config.id

        db.refresh(overlay_experience_config)
        assert overlay_experience_config.experiences.all() == [privacy_experience]

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "regions": [],
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        resp = response.json()["experience_config"]

        assert (
            resp["version"] == 1.0
        ), "Version not bumped because config didn't change, only region removed"
        assert resp["regions"] == []  # Main thing, regions were removed
        assert response.json()["linked_regions"] == []
        assert response.json()["unlinked_regions"] == ["us_tx"]

        db.refresh(overlay_experience_config)
        # ExperienceConfig was disabled - this is a change, so another historical record is created
        assert overlay_experience_config.histories.count() == 1
        experience_config_history = overlay_experience_config.histories[0]
        assert experience_config_history.version == 1.0
        assert experience_config_history.component == ComponentType.overlay
        assert (
            experience_config_history.experience_config_id
            == overlay_experience_config.id
        )

        # Updated Privacy Experience - TX Privacy Experience automatically *unlinked*
        assert overlay_experience_config.experiences.count() == 0
        db.refresh(privacy_experience)

        assert (
            privacy_experience.experience_config_id
            == "pri-7ae3-f06b-4096-970f-0bbbdef-over"
        )  # Default overlay experience config linked instead

        privacy_experience.delete(db)

    @pytest.mark.parametrize(
        "invalid_description",
        [
            (
                "This is a malicious description.<script>alert('XSS');</script> No scripts allowed!",
                "This is a malicious description. No scripts allowed!",
            ),
            (
                "This is a malicious <a href='javascript:alert('XSS')>description</a>.",
                "This is a malicious &lt;a rel=&quot;noopener noreferrer&quot;&gt;description&lt;/a&gt;.",
            ),
        ],
    )
    def test_update_experience_config_with_invalid_description(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        overlay_experience_config,
        invalid_description,
    ) -> None:
        """
        Verify that a malicious description is sanitized before saving.
        """
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "banner_description": invalid_description[0],
                "description": invalid_description[0],
            },
            headers=auth_header,
        )
        assert response.status_code == 200

        db.refresh(overlay_experience_config)
        assert overlay_experience_config.banner_description == invalid_description[1]
        assert overlay_experience_config.description == invalid_description[1]

    @pytest.mark.parametrize(
        "valid_description",
        [
            ("This is a valid description.", "This is a valid description."),
            (
                "This is a <strong>valid</strong> HTML description.",
                "This is a &lt;strong&gt;valid&lt;/strong&gt; HTML description.",
            ),
            (
                "This is a <strong>valid</strong> HTML description with a <a href='https://example.com/'>link</a>.",
                "This is a &lt;strong&gt;valid&lt;/strong&gt; HTML description with a &lt;a href=&quot;https://example.com/&quot; rel=&quot;noopener noreferrer&quot;&gt;link&lt;/a&gt;.",
            ),
        ],
    )
    def test_update_experience_config_with_valid_html_description(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
        db,
        overlay_experience_config,
        valid_description,
    ) -> None:
        """
        Verify that a valid description is saved.
        """
        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        response = api_client.patch(
            url,
            json={
                "banner_description": valid_description[0],
                "description": valid_description[0],
            },
            headers=auth_header,
        )
        assert response.status_code == 200

        db.refresh(overlay_experience_config)
        assert overlay_experience_config.banner_description == valid_description[1]
        assert overlay_experience_config.description == valid_description[1]

    @pytest.mark.usefixtures("privacy_experience_france_tcf_overlay")
    def test_add_regions_to_tcf_overlay(
        self,
        api_client: TestClient,
        generate_auth_header,
        experience_config_tcf_overlay,
        db,
    ) -> None:
        """Verify that regions can technically be added to the tcf overlay.

        This is a contrived example, but tests that this workflow doesn't break for the new tcf overlay
        """
        fr_experience = PrivacyExperience.get_experience_by_region_and_component(
            db=db, region="fr", component=ComponentType.tcf_overlay
        )
        assert fr_experience

        ca_experience = PrivacyExperience.get_experience_by_region_and_component(
            db=db, region="us_ca", component=ComponentType.tcf_overlay
        )
        assert not ca_experience

        auth_header = generate_auth_header(scopes=[scopes.PRIVACY_EXPERIENCE_UPDATE])
        url = V1_URL_PREFIX + EXPERIENCE_CONFIG + f"/{experience_config_tcf_overlay.id}"
        response = api_client.patch(
            url,
            json={
                "regions": ["us_ca", "fr"],
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        assert response.json()["experience_config"]["regions"] == ["fr", "us_ca"]
        assert response.json()["linked_regions"] == ["us_ca"]

        fr_experience = PrivacyExperience.get_experience_by_region_and_component(
            db=db, region="fr", component=ComponentType.tcf_overlay
        )
        assert fr_experience

        ca_experience = PrivacyExperience.get_experience_by_region_and_component(
            db=db, region="us_ca", component=ComponentType.tcf_overlay
        )
        assert ca_experience
