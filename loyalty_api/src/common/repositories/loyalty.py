import logging

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
    PromoHistoryResponse,
    PromoInput,
    PromoResponse,
)
from src.common.connectors.db import DbConnector
from src.common.exceptions import DatabaseError
from src.common.repositories import queries
from src.settings.loyalty_cards import LOYALTY_LEVELS


logger = logging.getLogger(__name__)


class LoyaltyRepository:
    def __init__(self, db: DbConnector):
        self._db = db

    async def create_promo(
        self, data: PromoInput, promo_code: str = None
    ) -> PromoResponse | None:
        try:
            row_data = await self._db.pool.fetchrow(
                queries.CREATE_PROMO,
                data.campaign_name,
                promo_code,
                data.products,
                data.type,
                data.value,
                data.duration,
                data.activation_date,
                data.activations_limit,
            )
        except Exception:
            logger.exception(
                "Failed to create a new promo: campaign_name %s products %s type %s",
                data.campaign_name,
                data.products,
                data.type,
                exc_info=True,
            )
            raise DatabaseError()
        return PromoResponse.parse_obj(row_data) if row_data else None

    async def create_user_promos(self, user_ids: set, promo_id: int):
        values = tuple((promo_id, user_id) for user_id in user_ids)
        try:
            return await self._db.pool.executemany(
                queries.CREATE_USER_PROMOS, values
            )
        except Exception:
            logger.exception(
                "Failed to create user promos: user_ids %s promo_id %s",
                user_ids,
                promo_id,
                exc_info=True,
            )
            raise DatabaseError()

    async def get_promo_by_promo_code(
        self, promo_code: str
    ) -> PromoResponse | None:
        row_data = await self._db.pool.fetchrow(
            queries.GET_PROMO_BY_PROMO_CODE, promo_code
        )
        return PromoResponse.parse_obj(row_data) if row_data else None

    async def get_promo_by_campaign_name(
        self, campaign_name: str
    ) -> list[PromoResponse]:
        rows = await self._db.pool.fetch(
            queries.GET_PROMO_BY_CAMPAIGN_NAME, campaign_name
        )
        return [PromoResponse.parse_obj(row_data) for row_data in rows]

    async def get_promo_activation(
        self, promo_id: int, user_id: str
    ) -> PromoActivateResponse | None:
        row_data = await self._db.pool.fetchrow(
            queries.GET_PROMO_ACTIVATION, promo_id, user_id
        )
        return PromoActivateResponse.parse_obj(row_data) if row_data else None

    async def create_promo_activation(self, promo_id: int, user_id: str):
        return await self._db.pool.execute(
            queries.CREATE_PROMO_ACTIVATION, promo_id, user_id
        )

    async def get_promo_activation_cnt(self, promo_id: int) -> int:
        return await self._db.pool.fetchval(
            queries.GET_ACTIVATIONS_COUNT, promo_id
        )

    async def set_flag_deactivated_promo(self, promo_id: int, flag: bool):
        return await self._db.pool.execute(
            queries.SET_FLAG_DEACTIVATED_PROMO, promo_id, flag
        )

    async def get_user_promo(self, user_id: str, promo_id: int) -> Record:
        row_data = await self._db.pool.fetchrow(
            queries.GET_USER_PROMO, promo_id, user_id
        )
        return row_data

    async def set_flag_linked_to_user(self, promo_id: int):
        return await self._db.pool.execute(
            queries.SET_FLAG_LINKED_TO_USER, promo_id
        )

    async def delete_user_promo_activation(self, promo_id: int, user_id: str):
        return await self._db.pool.execute(
            queries.DELETE_USER_PROMO_ACTIVATION, promo_id, user_id
        )

    async def get_promo_usage_history_by_promo_ids(
        self, promo_ids: list
    ) -> list[PromoHistoryResponse]:
        if not promo_ids:
            return []

        rows = await self._db.pool.fetch(
            queries.GET_PROMO_USAGE_HISTORY_BY_PROMO_IDS, promo_ids
        )
        return [PromoHistoryResponse.parse_obj(row_data) for row_data in rows]

    async def get_promo_usage_history_by_user_id(
        self, user_id: str
    ) -> list[PromoHistoryResponse]:
        rows = await self._db.pool.fetch(
            queries.GET_PROMO_USAGE_HISTORY_BY_USER_ID, user_id
        )
        return [PromoHistoryResponse.parse_obj(row_data) for row_data in rows]

    async def create_card(
        self, data: LoyaltyCardInput
    ) -> LoyaltyCardResponse | None:
        try:
            row_data = await self._db.pool.fetchrow(
                queries.CREATE_CARD,
                data.user_id,
                LOYALTY_LEVELS[0],
            )
        except Exception:
            logger.exception(
                "Failed to create a new loyalty card: user_id %s",
                data.user_id,
                exc_info=True,
            )
            raise DatabaseError()
        return LoyaltyCardResponse.parse_obj(row_data) if row_data else None

    async def get_loyalty_card_by_user_id(
        self, user_id: str
    ) -> LoyaltyCardResponse | None:
        row_data = await self._db.pool.fetchrow(
            queries.GET_PROMO_BY_PROMO_CODE, user_id
        )
        return LoyaltyCardResponse.parse_obj(row_data) if row_data else None

    async def get_loyalty_card_balance_by_user_id(
        self, user_id: str
    ) -> LoyaltyCardBalanceResponse | None:
        row_data = await self._db.pool.fetchrow(
            queries.GET_PROMO_BY_PROMO_CODE, user_id
        )
        return (
            LoyaltyCardBalanceResponse.parse_obj(row_data)
            if row_data
            else None
        )

    async def get_full_loyalty_info_by_user_id(
        self, user_id: str
    ) -> LoyaltyCardFullInfoResponse | None:
        row_data = await self._db.pool.fetchrow(
            queries.GET_LOYALTY_CARD_FULL_INFO, user_id
        )
        return (
            LoyaltyCardFullInfoResponse.parse_obj(row_data)
            if row_data
            else None
        )

    async def get_loyalty_card_balance_history_by_user_id(
        self, user_id: str
    ) -> list[LoyaltyCardBalanceHistoryResponse] | None:
        rows = await self._db.pool.fetch(
            queries.GET_PROMO_BY_PROMO_CODE, user_id
        )
        return [
            LoyaltyCardBalanceHistoryResponse.parse_obj(record)
            for record in rows
        ]

    async def loyalty_card_change_level(
        self, user_id: str, loyalty_level: int
    ) -> LoyaltyCardResponse | None:
        try:
            row_data = await self._db.pool.fetchrow(
                queries.CHANGE_LOYALTY_LEVEL,
                user_id,
                loyalty_level,
            )
        except Exception:
            logger.exception(
                "Failed to update loyalty level: user_id %s, loyalty_level %s",
                user_id,
                loyalty_level,
                exc_info=True,
            )
            raise DatabaseError()
        return LoyaltyCardResponse.parse_obj(row_data) if row_data else None

    async def refill_loyalty_card_points(
        self, data: PointsLoyaltyCardInput
    ) -> None:
        try:
            await self._db.pool.execute(
                queries.POINTS_LOYALTY_CARD,
                data.loyalty_id,
                data.user_id,
                data.points,
                data.source,
            )
        except Exception:
            logger.exception(
                "Failed to add points to card: user_id %s, points %s",
                data.user_id,
                data.points,
                exc_info=True,
            )
            raise DatabaseError()

    async def deduct_loyalty_card_points(
        self, data: PointsLoyaltyCardInput
    ) -> None:
        try:
            await self._db.pool.execute(
                queries.POINTS_LOYALTY_CARD,
                data.loyalty_id,
                data.user_id,
                -data.points,
                data.source,
            )
        except Exception:
            logger.exception(
                "Failed to deduct points from card: user_id %s, points %s",
                data.user_id,
                data.points,
                exc_info=True,
            )
            raise DatabaseError()
