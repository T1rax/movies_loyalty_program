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

        if data.user_ids:
            try:
                await self._repository.create_user_promos(
                    data.user_ids, promo.id
                )
                await self._repository.set_flag_linked_to_user(promo.id)
            except DatabaseError:
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Failed to create user promos.",
                )
        return promo

    async def promo_activate(self, promo_code: str, user_id: str):
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Сouldn't find a promo with this promo_code.",
            )

        if promo.linked_to_user:
            user_promo = await self._repository.get_user_promo(
                user_id, promo.id
            )
            if not user_promo:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="the promo code for the user was not found.",
                )

        promo_activation_cnt = await self._repository.get_promo_activation_cnt(
            promo.id
        )
        if promo_activation_cnt >= promo.activations_limit:
            await self._repository.deactivated_promo(promo.id)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The activation limit has been reached.",
            )

        user_promo_activation = await self._repository.get_promo_activation(
            promo.id, user_id
        )
        if user_promo_activation:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The user has already activated the promo.",
            )
        else:
            await self._repository.create_promo_activation(promo.id, user_id)

        return "Ok"
