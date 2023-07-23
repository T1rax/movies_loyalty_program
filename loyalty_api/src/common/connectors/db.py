import logging

import asyncpg
import ujson  # type: ignore[import]
from asyncpg import Connection, Pool
from src.settings import db_settings


logger = logging.getLogger(__name__)


async def register_json(conn: Connection):
    def _encoder(value):
        return b"\x01" + ujson.dumps(value).encode("utf-8")

    def _decoder(value):
        return ujson.loads(value[1:].decode("utf-8"))

    await conn.set_type_codec(
        "jsonb",
        encoder=_encoder,
        decoder=_decoder,
        schema="pg_catalog",
        format="binary",
    )
    await conn.set_type_codec(
        "json",
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema="pg_catalog",
    )


async def get_db():
    _db = DbConnector()
    return _db


class DbConnector:
    pool: Pool | None = None

    @staticmethod
    async def connect():
        try:
            DbConnector.pool = await asyncpg.create_pool(
                db_settings.db_url, init=register_json
            )
        except Exception:
            logger.exception("Db is not initialized", exc_info=True)

    @staticmethod
    async def disconnect():
        try:
            await DbConnector.pool.close()
        except Exception:
            logger.exception("Db is not disconnected", exc_info=True)
