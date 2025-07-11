import asyncio
import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status
from app import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://app.io") as test_client:
            yield test_client


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == {"hello": "world"}
