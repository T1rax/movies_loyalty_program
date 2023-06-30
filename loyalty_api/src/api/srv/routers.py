from fastapi import APIRouter
from src.api.srv.endpoints import technical


router = APIRouter(prefix="/api/srv", tags=["srv"])

router.include_router(technical.router)
