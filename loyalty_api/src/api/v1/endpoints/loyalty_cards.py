import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from src.api.models.loyalty_cards import (
    ChangeLoyaltyCardLevelInput,
    LoyaltyCardInput,
    PointsLoyaltyCardInput,
)
from src.common.decode_auth_token import get_decoded_data
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
    user_data=Depends(get_decoded_data),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await loyalty_cards_service.create_card(
        LoyaltyCardInput(user_id=user_id)
    )


@router.post(
    "/loyalty_cards/change_level",
    summary="Изменить уровень лояльности",
    description="Изменения уровня программы лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def change_loyalty_card_level(
    user_data=Depends(get_decoded_data),
    body: ChangeLoyaltyCardLevelInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    body.user_id = user_id
    return await loyalty_cards_service.change_level(body)


@router.get(
    "/loyalty_cards",
    summary="Получение информации по карте лояльности",
    description="Получение информации по карте лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def get_loyalty_card_full_info(
    user_data=Depends(get_decoded_data),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await loyalty_cards_service.get_card_info(user_id)


@router.get(
    "/loyalty_cards/history",
    summary="Получение истории карты лояльности",
    description="Получение логов истории пополнений/списаний карты лояльности",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def get_loyalty_card_balance_history(
    user_data=Depends(get_decoded_data),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

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
    user_data=Depends(get_decoded_data),
    body: PointsLoyaltyCardInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )
    body.user_id = user_id

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
    user_data=Depends(get_decoded_data),
    body: PointsLoyaltyCardInput = Body(...),
    loyalty_cards_service: LoyaltyCardsService = Depends(
        Provide[Container.loyalty_cards_service]
    ),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )
    body.user_id = user_id

    return await loyalty_cards_service.deduct_card_balance(body)
