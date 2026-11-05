import asyncio
import importlib.util
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import httpx
from fastapi.testclient import TestClient

spec = importlib.util.spec_from_file_location(
    "on_demand", Path(__file__).resolve().parents[1] / "scripts/on_demand.py"
)
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)


def test_cold_navigation_polls_and_mutations_are_not_replayed():
    with TestClient(gateway.app) as client, patch.object(
        gateway.launcher, "ready", AsyncMock(return_value=False)
    ), patch.object(gateway.launcher, "ensure_started") as start:
        response = client.get("/report/?session=abc", headers={"Accept": "text/html"})
        assert response.status_code == 200  # Cloudflare must preserve the startup page.
        assert "location.reload()" in response.text
        assert "/__chef_start_status" in response.text
        assert response.headers["cache-control"] == "no-store"
        response = client.post("/v1/action-log/mutations", json={"value": 1})
        assert response.status_code == 503
        assert response.headers["retry-after"] == "3"
        assert start.call_count == 2


def test_connector_health_does_not_wake_backend():
    with TestClient(gateway.app) as client, patch.object(gateway.launcher, "ensure_started") as start:
        assert client.get("/health").json()["service"] == "chef-core"
        start.assert_not_called()


def test_concurrent_requests_share_start_task():
    async def check():
        launcher = gateway.Launcher()
        launcher.start = AsyncMock()
        for _ in range(20):
            launcher.ensure_started(Mock())
        await launcher.task
        launcher.start.assert_awaited_once()
    asyncio.run(check())


def test_ready_proxy_preserves_auth_body_and_encoded_path():
    seen = []

    class Body(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b'{"saved":true}'

    async def upstream(request):
        seen.append((request.url, request.headers, await request.aread()))
        return httpx.Response(201, stream=Body(), headers={"Content-Type": "application/json"})

    with TestClient(gateway.app) as client, patch.object(
        gateway.launcher, "ready", AsyncMock(return_value=True)
    ):
        original = gateway.app.state.client
        gateway.app.state.client = httpx.AsyncClient(transport=httpx.MockTransport(upstream), verify=False)
        try:
            response = client.post("/v1/a%2Fb?q=1", content=b'{"value":1}',
                                   headers={"Authorization": "Bearer synthetic"})
            assert response.status_code == 201
            assert str(seen[0][0]) == "http://127.0.0.1:8801/v1/a%2Fb?q=1"
            assert seen[0][1]["authorization"] == "Bearer synthetic"
            assert seen[0][2] == b'{"value":1}'
            assert response.json() == {"saved": True}
        finally:
            gateway.app.state.client = original
