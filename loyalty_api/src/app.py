import sys

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from src.api import srv, v1
from src.common.connectors.db import DbConnector
from src.common.connectors.redis import RedisConnector
from src.common.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from src.common.ratelimiter import RateLimiter
from src.containers import Container
from src.settings import logger, settings


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    app = FastAPI(
        on_startup=[
            DbConnector.connect,
            RedisConnector.init_client,
            RateLimiter.init_ratelimiter,
        ],
        on_shutdown=[
            DbConnector.disconnect,
            RedisConnector.close_client,
            RateLimiter.close_ratelimiter,
        ],
        exception_handlers={
            HTTPException: http_exception_handler,
            RequestValidationError: request_validation_exception_handler,
        },
        title="Loyalty Api",
        openapi_url="/openapi.json",
        docs_url="/api/swagger",
        openapi_prefix="",
    )
    app.container = container

    app.include_router(srv.router)
    app.include_router(v1.router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.project_host,
        port=settings.project_port,
        log_config=logger.LOGGING,
        reload=True,
    )
