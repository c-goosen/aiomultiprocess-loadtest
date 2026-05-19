"""Integration tests against loadtest.test_server."""

from __future__ import annotations

import asyncio
import os

import httpx
import pytest

from loadtest.loadtest import (
    fetch,
    fetch_sync,
    run_aiomultiprocess,
    run_async_only,
    run_threaded,
)

BASE_URL = os.environ["TEST_BASE_URL"]
REQ_NUM = int(os.environ.get("TEST_REQ_NUM", "20"))


@pytest.mark.asyncio
async def test_fetch() -> None:
    status, body = await fetch(f"{BASE_URL}/")
    assert status == 200
    assert body["hello"] == "world"


def test_fetch_sync() -> None:
    status, body = fetch_sync(f"{BASE_URL}/")
    assert status == 200
    assert body["hello"] == "world"


@pytest.mark.asyncio
async def test_run_async_only() -> None:
    await run_async_only(req_num=REQ_NUM)


@pytest.mark.asyncio
async def test_run_aiomultiprocess() -> None:
    await run_aiomultiprocess(req_num=REQ_NUM)


def test_run_threaded() -> None:
    run_threaded(req_num=REQ_NUM)


def test_server_health() -> None:
    response = httpx.get(f"{BASE_URL}/", timeout=5.0)
    assert response.status_code == 200
    assert response.json()["hello"] == "world"
