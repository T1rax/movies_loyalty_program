import logging
from http import HTTPStatus

from fastapi import HTTPException
from src.api.models.promo import PromoInput, PromoResponse
from src.common.exceptions import DatabaseError
from src.common.promo import get_promo_code
from src.common.repositories.loyalty import LoyaltyRepository


logger = logging.getLogger(__name__)


class LoyaltyService:
    def __init__(
        self,
        repository: LoyaltyRepository,
    ):
        self._repository = repository

    async def create_promo(self, data: PromoInput) -> PromoResponse | None:
        promo_code = get_promo_code()

        try:
            promo = await self._repository.create_promo(data, promo_code)
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new promo.",
            )
        return promo

    async def promo_activate(self, promo_code: str, user_id: str):
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Сouldn't find a promo with this promo_code.",
            )

        if promo.user_ids and user_id not in promo.user_ids:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Promo_code for user_id not found.",
            )

        promo_activation = await self._repository.get_promo_activation(
            promo.id, user_id
        )
        if (
            promo_activation
            and promo_activation.activations_cnt >= promo.activations_limit
        ):
            await self._repository.deactivated_promo(promo.id)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The activation limit has been reached.",
            )

        if promo_activation:
            activations_cnt = promo_activation.activations_cnt + 1
            await self._repository.set_activations_count(
                activations_cnt, promo.id, user_id
            )
        else:
            activations_cnt = 1
            await self._repository.create_promo_activation(
                promo.id, user_id, activations_cnt
            )

        return "Ok"
