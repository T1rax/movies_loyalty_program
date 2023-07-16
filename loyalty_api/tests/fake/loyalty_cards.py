from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from src.api.models.loyalty_cards import (
    ChangeLoyaltyCardLevelInput,
    LoyaltyCardInput,
    LoyaltyCardLevelActions,
    LoyaltyCardResponse,
)


class FakeLoyaltyCardsService:
    async def create_card(
        self, data: LoyaltyCardInput
    ) -> LoyaltyCardResponse | None:
        response = LoyaltyCardResponse(
            id="12345",
            user_id=data.user_id,
            loyalty_level=5,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    def up_loyalty_level(self, current_level: int) -> int:
        return current_level + 1

    def down_loyalty_level(self, current_level: int) -> int:
        return current_level - 1

    async def change_level(
        self, data: ChangeLoyaltyCardLevelInput
    ) -> LoyaltyCardResponse | None:
        loyalty_card = LoyaltyCardResponse(
            id="12345",
            user_id=data.user_id,
            loyalty_level=5,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
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
                loyalty_level = data.loyalty_level
            case _:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Not supported action",
                )

        loyalty_card.loyalty_level = loyalty_level
        return loyalty_card
