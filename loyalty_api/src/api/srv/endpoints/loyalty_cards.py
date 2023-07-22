from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from src import settings
from src.api.models.loyalty_cards import (
    ChangeLoyaltyCardLevelInput,
    LoyaltyCardInput,
    PointsLoyaltyCardInput,
)
from src.common.responses import ApiResponse, wrap_response
from src.common.services.loyalty_cards import LoyaltyCardsService
from src.containers import Container
from starlette import status


router = APIRouter()


@router.post(
    "/loyalty_cards",
    summary="Создать карту лояльности",
    description="Ручка создания карты лояльности для пользователя.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def create_loyalty_card(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: LoyaltyCardInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_cards_service.create_card(body)


@router.post(
    "/loyalty_cards/change_level",
    summary="Изменить уровень лояльности",
    description="Изменения уровня программы лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def change_loyalty_card_level(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: ChangeLoyaltyCardLevelInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
    if not body.user_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "user_id is not provided"
        )

    return await loyalty_cards_service.change_level(body)


@router.get(
    "/loyalty_cards/{user_id}",
    summary="Получение информации по карте лояльности",
    description="Получение информации по карте лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def get_loyalty_card_full_info(
    user_id: str,
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_cards_service.get_card_info(user_id)


@router.get(
    "/loyalty_cards/history/{user_id}",
    summary="Получение истории карты лояльности",
    description="Получение логов истории пополнений/списаний карты лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def get_loyalty_card_balance_history(
    user_id: str,
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await loyalty_cards_service.get_points_history(user_id)


@router.post(
    "/loyalty_cards/refill",
    summary="Пополнение карты лояльности",
    description="Пополнение баланса карты лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def refill_loyalty_card_balance(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: PointsLoyaltyCardInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
    if not body.user_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "user_id is not provided"
        )

    return await loyalty_cards_service.refill_card(body)


@router.post(
    "/loyalty_cards/deduct",
    summary="Списание с карты лояльности",
    description="Списание баланса карты лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def deduct_loyalty_card_balance(
    token_header: str
    | None = Header(None, alias=settings.token_settings.token_header),
    body: PointsLoyaltyCardInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in settings.LOYALTY_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
    if not body.user_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "user_id is not provided"
        )

    return await loyalty_cards_service.deduct_card_balance(body)
