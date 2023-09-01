import pytest

from constants_nox import DEV_TAG_SUFFIX, PRERELEASE_TAG_SUFFIX, RC_TAG_SUFFIX
from docker_nox import generate_buildx_command


class TestGenerateBuildxCommand:
    def test_single_tag(self) -> None:
        actual_result = generate_buildx_command(
            image_tags=["foo"],
            docker_build_target="prod",
            platform="linux/amd64",
            dockerfile_path=".",
        )
        expected_result = (
            "docker",
            "buildx",
            "build",
            "--push",
            "--target=prod",
            "--platform",
            "linux/amd64",
            ".",
            "--tag",
            "foo",
        )
        assert actual_result == expected_result

    def test_multiplte_tags(self) -> None:
        actual_result = generate_buildx_command(
            image_tags=["foo", "bar"],
            docker_build_target="prod",
            platform="linux/arm64",
            dockerfile_path=".",
        )
        expected_result = (
            "docker",
            "buildx",
            "build",
            "--push",
            "--target=prod",
            "--platform",
            "linux/arm64",
            ".",
            "--tag",
            "foo",
            "--tag",
            "bar",
        )
        assert actual_result == expected_result

    def test_different_path(self) -> None:
        actual_result = generate_buildx_command(
            image_tags=["foo", "bar"],
            docker_build_target="prod",
            dockerfile_path="other_path",
            platform="linux/arm64",
        )
        expected_result = (
            "docker",
            "buildx",
            "build",
            "--push",
            "--target=prod",
            "--platform",
            "linux/arm64",
            "other_path",
            "--tag",
            "foo",
            "--tag",
            "bar",
        )
        assert actual_result == expected_result
