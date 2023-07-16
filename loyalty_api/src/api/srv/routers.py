from fastapi import APIRouter
from src.api.srv.endpoints import loyalty_cards, promos, technical


router = APIRouter(prefix="/api/srv", tags=["srv"])

router.include_router(technical.router)
router.include_router(promos.router)
router.include_router(loyalty_cards.router)
