import pytest
from httpx import ASGITransport, AsyncClient

from database import engine
from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    if engine.url.database != "supportflow_test":
        raise RuntimeError("Use supportflow_test")

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as http_client:
            yield http_client
    finally:
        await engine.dispose()


@pytest.fixture
def contact_payload():
    return {
        "name": "Ayesha",
        "phones": [{"number": "03001234567"}],
    }
