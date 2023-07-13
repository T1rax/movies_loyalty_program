import logging

from asyncpg import Record
from src.api.models.promo import (
    PromoActivateResponse,
    PromoInput,
    PromoResponse,
)
from src.common.connectors.db import DbConnector
from src.common.exceptions import DatabaseError
from src.common.repositories import queries


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

    async def get_promo_activation_cnt(self, promo_id: int):
        return await self._db.pool.execute(
            queries.GET_ACTIVATIONS_COUNT, promo_id
        )

    async def deactivated_promo(self, promo_id: int):
        return await self._db.pool.execute(
            queries.SET_DEACTIVATED_PROMO, promo_id
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
