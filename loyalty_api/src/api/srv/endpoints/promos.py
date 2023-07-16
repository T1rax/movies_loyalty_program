from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from src import settings
from src.api.models.promo import (
    PromoActivateInputSrv,
    PromoDeactivateInputSrv,
    PromoHistoryParam,
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
    "/v1/promos/deactivate",
    summary="Деактивировать промокод.",
    description="Ручка для деактивации промокода. "
    "Промокод больше не будет действовать, но и не будет удален из БД.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_deactivate(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: PromoDeactivateInputSrv = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_service.promo_deactivate(body.promo_code)


@router.get(
    "/v1/promos/history",
    summary="",
    description="",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_history(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    param: PromoHistoryParam = Depends(),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_service.promo_history(param)
