from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from fastapi_limiter.depends import RateLimiter
from src import settings
from src.api.models.promo import (
    GetPromoStatusInputSrv,
    PromoActivateInputSrv,
    PromoInput,
    PromoRestoreInputSrv,
)
from src.common.responses import ApiResponse, wrap_response
from src.common.services.loyalty import LoyaltyService
from src.containers import Container
from starlette import status


router = APIRouter()


@router.post(
    "/v1/promos",
    summary="Создать промо-акцию.",
    description="Ручка создания промокода/скидки на какой-либо продукт.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def create_promo(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: PromoInput = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_service.create_promo(body)


@router.post(
    "/v1/promos/activate",
    summary="Применить промокод.",
    description="Ручка для применения/использования промокода/скидки.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_activate(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: PromoActivateInputSrv = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_service.promo_activate(body.promo_code, body.user_id)


@router.post(
    "/v1/promos/restore",
    summary="Восстановить промокод.",
    description="Ручка для восстановления промокода/скидки.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_restore(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: PromoRestoreInputSrv = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_service.promo_restore(body.promo_code, body.user_id)


@router.post(
    "/v1/promos/status",
    summary="Получить статус возможности применения промокода.",
    description="Ручка для получения статуса возможности применения промокода/скидки.",
    response_model=ApiResponse,
    dependencies=[Depends(RateLimiter(times=20, minutes=1))],
)
@inject
@wrap_response
async def get_promo_status(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: GetPromoStatusInputSrv = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_service.get_promo_status(
        body.promo_code, body.user_id
    )
