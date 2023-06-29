from fastapi import APIRouter, Depends
from src.common.connectors.db import get_db


router = APIRouter()


@router.get("/ping")
def ping():
    return {"result": "pong"}


@router.get("/db")
async def db_version(db=Depends(get_db)):
    return {"version": await db.pool.fetchval("SELECT version();")}
