import logging
from http import HTTPStatus

from fastapi import HTTPException
from fastapi_pagination import paginate
from src.api.models.promo import (
    PromoHistoryFilterListing,
    PromoInput,
    PromoResponse,
)
from src.common.exceptions import DatabaseError
from src.common.promo import get_promo_code
from src.common.repositories.loyalty import LoyaltyRepository


logger = logging.getLogger(__name__)


class PromosService:
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

    async def promo_activate(self, promo_code: str, user_id: str) -> str:
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo or promo.deactivated:
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
                    detail="Promo_code for user not found.",
                )

        promo_activation_cnt = await self._repository.get_promo_activation_cnt(
            promo.id
        )
        if promo_activation_cnt >= promo.activations_limit:
            await self._repository.set_flag_deactivated_promo(promo.id, True)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Activation limit has been reached.",
            )

        user_promo_activation = await self._repository.get_promo_activation(
            promo.id, user_id
        )
        if user_promo_activation:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="User has already activated promo.",
            )
        await self._repository.create_promo_activation(promo.id, user_id)

        return "Ok"

    async def promo_restore(self, promo_code: str, user_id: str) -> str:
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Promo not found.",
            )

        user_promo_activation = await self._repository.get_promo_activation(
            promo.id, user_id
        )
        if not user_promo_activation:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User did not activate this promo_code.",
            )

        await self._repository.delete_user_promo_activation(promo.id, user_id)
        if promo.deactivated:
            await self._repository.set_flag_deactivated_promo(promo.id, False)

        return "Ok"

    async def get_promo_status(self, promo_code: str, user_id: str):
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo or promo.deactivated:
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
                    detail="Promo_code for user not found.",
                )

        promo_activation_cnt = await self._repository.get_promo_activation_cnt(
            promo.id
        )
        if promo_activation_cnt >= promo.activations_limit:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Activation limit has been reached.",
            )

        user_promo_activation = await self._repository.get_promo_activation(
            promo.id, user_id
        )
        if user_promo_activation:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="User has already activated promo.",
            )

        return "Ok"

    async def promo_deactivate(self, promo_code: str) -> str:
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Сouldn't find a promo with this promo_code.",
            )
        if promo.deactivated:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The promo_code has already been deactivated.",
            )

        await self._repository.set_flag_deactivated_promo(promo.id, True)

        return "Ok"

    async def get_promo_usage_history(
        self, query_param: PromoHistoryFilterListing
    ):
        promo_usage_history = []

        if query_param.promo_id:
            promo_usage_history = (
                await self._repository.get_promo_usage_history_by_promo_ids(
                    [query_param.promo_id]
                )
            )

        if not query_param.promo_id and query_param.campaign_name:
            promos = await self._repository.get_promo_by_campaign_name(
                query_param.campaign_name
            )
            promo_ids = [promo.id for promo in promos]
            promo_usage_history = (
                await self._repository.get_promo_usage_history_by_promo_ids(
                    promo_ids
                )
            )

        if query_param.user_id and (
            query_param.promo_id or query_param.campaign_name
        ):
            promo_usage_history = list(
                filter(
                    lambda promo_usage: str(promo_usage.user_id)
                    == query_param.user_id,
                    promo_usage_history,
                )
            )

        if (
            query_param.user_id
            and not query_param.promo_id
            and not query_param.campaign_name
        ):
            promo_usage_history = (
                await self._repository.get_promo_usage_history_by_user_id(
                    query_param.user_id
                )
            )

        return paginate(sequence=promo_usage_history)

    async def get_promo_info(self, promo_code: str):
        promo = await self._repository.get_promo_by_promo_code(promo_code)
        if not promo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Сouldn't find a promo with this promo_code.",
            )

        return promo
