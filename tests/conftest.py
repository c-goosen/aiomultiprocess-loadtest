"""Pytest configuration for integration tests."""

from __future__ import annotations

import os

import pytest


def pytest_configure(config: pytest.Config) -> None:
    if "TEST_BASE_URL" not in os.environ:
        pytest.exit(
            "TEST_BASE_URL is not set. Run tests via `make test` "
            "or start the server with `make server` and export TEST_BASE_URL.",
            returncode=2,
        )
