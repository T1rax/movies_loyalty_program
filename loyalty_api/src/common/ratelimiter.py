import logging

from fastapi_limiter import FastAPILimiter
from src.common.connectors.redis import RedisConnector


logger = logging.getLogger(__name__)


class RateLimiter:
    ratelimiter: FastAPILimiter | None = None

    @staticmethod
    async def init_ratelimiter():
        try:
            RateLimiter.ratelimiter = await FastAPILimiter.init(
                RedisConnector.client
            )
        except Exception:
            logger.error("Ratelimiter is not initialized", exc_info=True)

    @staticmethod
    async def close_ratelimiter():
        try:
            await RateLimiter.ratelimiter.close()
        except Exception:
            logger.error("Ratelimiter is not closed", exc_info=True)
