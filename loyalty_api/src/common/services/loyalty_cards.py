import logging
from http import HTTPStatus

from fastapi import HTTPException
from src.api.models.loyalty_cards import (
    ChangeLoyaltyCardLevelInput,
    LoyaltyCardBalanceHistoryResponse,
    LoyaltyCardFullInfoResponse,
    LoyaltyCardInput,
    LoyaltyCardLevelActions,
    LoyaltyCardResponse,
    PointsLoyaltyCardInput,
)
from src.common.exceptions import DatabaseError
from src.common.repositories.loyalty import LoyaltyRepository
from src.settings.loyalty_cards import LOYALTY_LEVELS


logger = logging.getLogger(__name__)


class LoyaltyCardsService:
    def __init__(
        self,
        repository: LoyaltyRepository,
    ):
        self._repository = repository

    async def create_card(
        self, data: LoyaltyCardInput
    ) -> LoyaltyCardResponse | None:
        try:
            loyalty_card = await self._repository.get_loyalty_card_by_user_id(
                data.user_id
            )
            if loyalty_card:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="User already has loyalty card.",
                )

            loyalty_card = await self._repository.create_card(data)
            return loyalty_card
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create new loyalty card.",
            )

    def up_loyalty_level(self, current_level: int) -> int:
        try:
            index = LOYALTY_LEVELS.index(current_level)
            new_level = LOYALTY_LEVELS[index + 1]
            return new_level
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Unable to increase user's loyalty level",
            )

    def down_loyalty_level(self, current_level: int) -> int:
        try:
            index = LOYALTY_LEVELS.index(current_level)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Unable to increase user's loyalty level",
            )

        if index == 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="User already has lowest level",
            )

        new_level = LOYALTY_LEVELS[index - 1]
        return new_level

    async def change_level(
        self, data: ChangeLoyaltyCardLevelInput
    ) -> LoyaltyCardResponse | None:
        try:
            loyalty_card = await self._repository.get_loyalty_card_by_user_id(
                data.user_id
            )
            if not loyalty_card:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="User does not have loyalty card",
                )

            match data.action:
                case LoyaltyCardLevelActions.UP:
                    loyalty_level = self.up_loyalty_level(
                        loyalty_card.loyalty_level
                    )
                case LoyaltyCardLevelActions.DOWN:
                    loyalty_level = self.down_loyalty_level(
                        loyalty_card.loyalty_level
                    )
                case LoyaltyCardLevelActions.EXACT:
                    if data.loyalty_level not in LOYALTY_LEVELS:
                        raise HTTPException(
                            status_code=HTTPStatus.BAD_REQUEST,
                            detail="Not supported loyalty level",
                        )
                    loyalty_level = data.loyalty_level
                case _:
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_REQUEST,
                        detail="Not supported action",
                    )

            loyalty_card = await self._repository.loyalty_card_change_level(
                data.user_id, loyalty_level
            )
            return loyalty_card
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create new loyalty card.",
            )

    async def get_card_info(
        self, user_id: str
    ) -> LoyaltyCardFullInfoResponse | None:
        try:
            return await self._repository.get_full_loyalty_info_by_user_id(
                user_id
            )
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to find loyalty card",
            )

    async def get_points_history(
        self, user_id: str
    ) -> list[LoyaltyCardBalanceHistoryResponse] | None:
        try:
            return await self._repository.get_loyalty_card_balance_history_by_user_id(
                user_id
            )
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to find loyalty card",
            )

    async def refill_card(self, data: PointsLoyaltyCardInput) -> str:
        try:
            loyalty_card = await self._repository.get_loyalty_card_by_user_id(
                data.user_id
            )
            if not loyalty_card:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="User does not have loyalty card",
                )

            data.loyalty_id = loyalty_card.id

            await self._repository.refill_loyalty_card_points(data)
            return "success"
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create new loyalty card.",
            )

    async def deduct_card_balance(self, data: PointsLoyaltyCardInput) -> str:
        try:
            loyalty_card = await self._repository.get_loyalty_card_by_user_id(
                data.user_id
            )
            if not loyalty_card:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="User does not have loyalty card",
                )

            data.loyalty_id = loyalty_card.id

            await self._repository.deduct_loyalty_card_points(data)
            return "success"
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create new loyalty card.",
            )
