import logging

from redis import asyncio as aioredis
from redis.asyncio import Redis
from src.settings import redis_settings


logger = logging.getLogger(__name__)


def get_redis() -> Redis:
    _redis = RedisConnector()
    return _redis


class RedisConnector:
    client: Redis | None = None

    @staticmethod
    async def init_client():
        try:
            RedisConnector.client = await aioredis.from_url(
                f"redis://{redis_settings.redis_host}:{redis_settings.redis_port}",
                encoding="utf-8",
                decode_responses=True,
            )
        except Exception:
            logger.error("Redis client is not initialized", exc_info=True)

    @staticmethod
    async def close_client():
        try:
            await RedisConnector.client.close()
        except Exception:
            logger.error("Redis client is not closed", exc_info=True)
