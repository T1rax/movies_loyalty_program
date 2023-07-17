import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from src.api.models.promo import (
    PromoActivateInput,
    PromoRestoreInput,
    PromoStatusInput,
)
from src.common.decode_auth_token import get_decoded_data
from src.common.responses import ApiResponse, wrap_response
from src.common.services.loyalty import LoyaltyService
from src.containers import Container
from starlette import status


router = APIRouter()


@router.post(
    "/promos/activate",
    summary="Применить промокод.",
    description="Ручка для применения/использования промокода/скидки.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_activate(
    user_data=Depends(get_decoded_data),
    body: PromoActivateInput = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await loyalty_service.promo_activate(body.promo_code, user_id)


@router.post(
    "/promos/restore",
    summary="Восстановить промокод.",
    description="Ручка для восстановления промокода/скидки.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_restore(
    user_data=Depends(get_decoded_data),
    body: PromoRestoreInput = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await loyalty_service.promo_restore(body.promo_code, user_id)


@router.post(
    "/promos/status",
    summary="Получить статус промокода.",
    description="Ручка для получения статуса промокода/скидки.",
    response_model=ApiResponse,
    dependencies=[Depends(RateLimiter(times=20, minutes=1))],
)
@inject
@wrap_response
async def promo_status(
    body: PromoStatusInput = Body(...),
    loyalty_service: LoyaltyService = Depends(
        Provide[Container.loyalty_service]
    ),
):
    return await loyalty_service.promo_status(body.promo_code, body.user_id)
