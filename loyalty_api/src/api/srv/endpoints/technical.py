from fastapi import APIRouter, Depends
from src.common.connectors.db import get_db
from src.common.connectors.redis import get_redis


router = APIRouter()


@router.get("/ping")
def ping():
    return {"result": "pong"}


@router.get("/db")
async def db_version(db=Depends(get_db)):
    return {"version": await db.pool.fetchval("SELECT version();")}


@router.get("/redis")
async def redis_ping(redis=Depends(get_redis)):
    return {"ping": await redis.client.get("ping")}
