from collections import OrderedDict

from src.api.models.promo import (
    PromoActivateResponse,
    PromoHistoryResponse,
    PromoResponse,
    PromoType,
)
from src.common.repositories import queries


test_products = ["product_1", "product_2"]


async def _insert_promo(pool, test_data: dict):
    row_data = await pool.fetchrow(queries.CREATE_PROMO, *test_data.values())
    return row_data


async def _insert_user_promos(pool, user_ids: set, promo_id: int):
    values = tuple((promo_id, user_id) for user_id in user_ids)
    row_data = await pool.executemany(queries.CREATE_USER_PROMOS, values)
    return row_data


async def _insert_promo_activation(pool, test_data: dict):
    row_data = await pool.fetchrow(
        """
        INSERT INTO promos_activations (promo_id, user_id)
        VALUES ($1, $2)
        RETURNING *;
        """,
        *test_data.values(),
    )
    return row_data


async def get_promo_by_id(pool, promo_id: int):
    row_data = await pool.fetchrow(
        """
        SELECT id, campaign_name, promo_code, products, "type", "value", duration, activation_date, activations_limit, linked_to_user, deactivated, created_dt, updated_dt
        FROM promos
        WHERE id=$1;
        """,
        promo_id,
    )
    return PromoResponse.parse_obj(row_data) if row_data else None


async def create_promo(
    pool,
    campaign_name="test",
    products=None,
    type=PromoType.DISCOUNT.value,
    value=10,
    duration=None,
    activation_date=None,
    user_ids=None,
    activations_limit=1,
    promo_code=None,
):
    if not products:
        products = test_products
    test_data = OrderedDict(
        campaign_name=campaign_name,
        promo_code=promo_code,
        products=products,
        type=type,
        value=value,
        duration=duration,
        activation_date=activation_date,
        activations_limit=activations_limit,
    )
    row_data = await _insert_promo(pool, test_data)

    if user_ids:
        await _insert_user_promos(pool, user_ids, row_data.get("id"))
        await pool.execute(queries.SET_FLAG_LINKED_TO_USER, row_data.get("id"))

    return PromoResponse.parse_obj(row_data) if row_data else None


def get_promos_response(
    id=1,
    campaign_name="test",
    promo_code=None,
    products=None,
    type=None,
    value=None,
    duration=None,
    activation_date=None,
    activations_limit=1,
    deactivated=False,
    created_dt=None,
    updated_dt=None,
    linked_to_user=False,
):
    if activation_date:
        activation_date = activation_date.isoformat()
    if created_dt:
        created_dt = created_dt.isoformat()
    if updated_dt:
        updated_dt = updated_dt.isoformat()
    return {
        "success": True,
        "result": {
            "id": id,
            "campaign_name": campaign_name,
            "promo_code": promo_code,
            "products": products,
            "type": type,
            "value": value,
            "duration": duration,
            "activation_date": activation_date,
            "activations_limit": activations_limit,
            "deactivated": deactivated,
            "created_dt": created_dt,
            "updated_dt": updated_dt,
            "linked_to_user": linked_to_user,
        },
        "errors": None,
    }


async def create_promo_activation(
    pool,
    promo_id=1,
    user_id="a1bee0ec-02a2-42cf-9aa6-ee82835aabaf",
):
    test_data = OrderedDict(
        promo_id=promo_id,
        user_id=user_id,
    )
    row_data = await _insert_promo_activation(pool, test_data)

    return PromoActivateResponse.parse_obj(row_data) if row_data else None


async def get_promo_activation(pool, promo_id: int, user_id: str):
    row_data = await pool.fetchrow(
        queries.GET_PROMO_ACTIVATION, promo_id, user_id
    )
    return PromoActivateResponse.parse_obj(row_data) if row_data else None


async def delete_user_promo_activation(pool, promo_id: int, user_id: str):
    return await pool.execute(
        queries.DELETE_USER_PROMO_ACTIVATION, promo_id, user_id
    )


async def set_flag_deactivated_promo(pool, promo_id: int, flag: bool):
    return await pool.execute(
        queries.SET_FLAG_DEACTIVATED_PROMO, promo_id, flag
    )


async def get_promo_usage_history_by_promo_ids(
    pool, promo_ids: list
) -> list[PromoHistoryResponse]:
    if not promo_ids:
        return []

    rows = await pool.fetch(
        queries.GET_PROMO_USAGE_HISTORY_BY_PROMO_IDS, promo_ids
    )
    return [PromoHistoryResponse.parse_obj(row_data) for row_data in rows]
