import logging
from datetime import datetime

from asyncpg import Record
from src.api.models.loyalty_cards import (
    LoyaltyCardBalanceHistoryResponse,
    LoyaltyCardBalanceResponse,
    LoyaltyCardFullInfoResponse,
    LoyaltyCardInput,
    LoyaltyCardResponse,
    PointsLoyaltyCardInput,
)
from src.api.models.promo import (
    PromoActivateResponse,
    PromoInput,
    PromoResponse,
    PromoType,
)


logger = logging.getLogger(__name__)


class FakeLoyaltyRepository:
    async def create_promo(
        self, data: PromoInput, promo_code: str = None
    ) -> PromoResponse | None:
        response = PromoResponse(
            id=12345,
            campaign_name=data.campaign_name,
            promo_code=promo_code,
            products=data.products,
            type=data.type,
            value=data.value,
            linked_to_user=True,
            duration=data.duration,
            activation_date=data.activation_date,
            activations_limit=data.activations_limit,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    async def create_user_promos(self, user_ids: set, promo_id: int):
        pass

    async def get_promo_by_promo_code(
        self, promo_code: str
    ) -> PromoResponse | None:
        response = PromoResponse(
            id=12345,
            campaign_name="promo_campaign",
            promo_code=promo_code,
            products=["test_product"],
            type=PromoType.DISCOUNT,
            value=30,
            linked_to_user=True,
            duration=30,
            activation_date=datetime.now(),
            activations_limit=30,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    async def get_promo_activation(
        self, promo_id: int, user_id: str
    ) -> PromoActivateResponse | None:
        pass

    async def create_promo_activation(self, promo_id: int, user_id: str):
        pass

    async def get_promo_activation_cnt(self, promo_id: int):
        pass

    async def deactivated_promo(self, promo_id: int):
        pass

    async def get_user_promo(self, user_id: str, promo_id: int) -> Record:
        pass

    async def set_flag_linked_to_user(self, promo_id: int):
        pass

    async def create_card(
        self, data: LoyaltyCardInput
    ) -> LoyaltyCardResponse | None:
        response = LoyaltyCardResponse(
            id="loyalty_id_12345",
            user_id=data.user_id,
            loyalty_level=5,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    async def get_loyalty_card_by_user_id(
        self, user_id: str
    ) -> LoyaltyCardResponse | None:
        if user_id == 'test_create_uuid':
            return None

        response = LoyaltyCardResponse(
            id="loyalty_id_12345",
            user_id=user_id,
            loyalty_level=5,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    async def get_loyalty_card_balance_by_user_id(
        self, user_id: str
    ) -> LoyaltyCardBalanceResponse | None:
        response = LoyaltyCardBalanceResponse(
            loyalty_id="loyalty_id_12345",
            user_id=user_id,
            balance=100,
        )
        return response

    async def get_full_loyalty_info_by_user_id(
        self, user_id: str
    ) -> LoyaltyCardFullInfoResponse | None:
        response = LoyaltyCardFullInfoResponse(
            loyalty_id="loyalty_id_12345",
            user_id=user_id,
            loyalty_level=5,
            balance=100,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    async def get_loyalty_card_balance_history_by_user_id(
        self, user_id: str
    ) -> list[LoyaltyCardBalanceHistoryResponse] | None:
        record1 = LoyaltyCardBalanceHistoryResponse(
            id="1",
            points=100,
            source="purchase",
            created_dt=datetime.now(),
        )
        record2 = LoyaltyCardBalanceHistoryResponse(
            id="2",
            points=500,
            source="promo",
            created_dt=datetime.now(),
        )
        return [record1, record2]

    async def loyalty_card_change_level(
        self, user_id: str, loyalty_level: int
    ) -> LoyaltyCardResponse | None:
        response = LoyaltyCardResponse(
            id="12345",
            user_id=user_id,
            loyalty_level=loyalty_level,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )
        return response

    async def refill_loyalty_card_points(
        self, data: PointsLoyaltyCardInput
    ) -> None:
        pass

    async def deduct_loyalty_card_points(
        self, data: PointsLoyaltyCardInput
    ) -> None:
        pass
