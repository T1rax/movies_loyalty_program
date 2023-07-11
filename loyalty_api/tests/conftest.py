import subprocess
from urllib.parse import urlsplit

import asyncpg
import psycopg2
import pytest
import pytest_asyncio
from httpx import AsyncClient
from src.app import create_app
from src.common.connectors.db import register_json


DATABASE_URL = "postgresql://app:123qwe@localhost:6668/loyalty"


@pytest_asyncio.fixture
async def test_app():
    app = create_app()
    yield app


@pytest_asyncio.fixture
async def test_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


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
