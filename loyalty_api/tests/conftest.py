import asyncio
import subprocess
from urllib.parse import urlsplit

import asyncpg
import psycopg2
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi_limiter import FastAPILimiter
from httpx import AsyncClient
from redis import asyncio as aioredis
from src.app import create_app
from src.common.connectors.db import register_json
from src.common.decode_auth_token import get_decoded_data
from src.settings.tokens import token_settings
from tests.fake.jwt import fake_decode_token


DATABASE_URL = "postgresql://app:123qwe@localhost:6668/loyalty"
REDIS_URL = "redis://localhost:8040"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def test_app():
    app = create_app()
    yield app


@pytest_asyncio.fixture(scope="session")
async def test_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def redis_client():
    client = await aioredis.from_url(
        url=REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    yield client


@pytest_asyncio.fixture
async def fastapi_limiter(redis_client):
    await FastAPILimiter.init(redis_client)


@pytest_asyncio.fixture
async def flush_redis(redis_client):
    await redis_client.flushdb()


@pytest_asyncio.fixture(scope="session", autouse=True)
def migrations():
    assert urlsplit(DATABASE_URL).path == "/loyalty"
    subprocess.run(
        [
            "yoyo",
            "apply",
            "--no-config-file",
            "--database",
            DATABASE_URL,
            "./migrations",
            "-b",
        ],
        capture_output=True,
        check=True,
    )


@pytest.fixture
def clean_table(request):
    def teardown():
        clean_tables(*request.param)

    request.addfinalizer(teardown)


def clean_tables(*tables):
    conn = psycopg2.connect(DATABASE_URL)
    for table in tables:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM %s" % table)
    conn.commit()


@pytest_asyncio.fixture
async def pool():
    pool = await asyncpg.create_pool(DATABASE_URL, init=register_json)
    yield pool
    await pool.close()


@pytest_asyncio.fixture(scope="session")
async def test_api_client(test_app):
    test_app.dependency_overrides[get_decoded_data] = fake_decode_token

    client = TestClient(test_app)
    default_headers = dict()
    default_headers[token_settings.token_header] = "test"
    client.headers = default_headers
    yield client
