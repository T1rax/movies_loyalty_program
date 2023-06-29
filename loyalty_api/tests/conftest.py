import pytest_asyncio
from httpx import AsyncClient
from src.app import create_app


@pytest_asyncio.fixture
async def test_app():
    app = create_app()
    yield app


@pytest_asyncio.fixture
async def test_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client
