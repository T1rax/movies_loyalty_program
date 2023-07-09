import logging

from src.api.models.promo import PromoInput, PromoResponse
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
                data.user_ids,
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

    async def get_promo_by_promo_code(
        self, promo_code: str
    ) -> PromoResponse | None:
        row_data = await self._db.pool.fetchrow(
            queries.GET_PROMO_BY_PROMO_CODE, promo_code
        )
        return PromoResponse.parse_obj(row_data) if row_data else None

    async def get_promo_activation(self, promo_id: int, user_id: str):
        pass

    async def create_promo_activation(self, promo_id: int, user_id: str):
        pass

    async def set_activations_count(
        self, activations_cnt: int, promo_id: int, user_id: str
    ):
        pass

    async def deactivated_promo(self, promo_id: int, user_id: str):
        pass
