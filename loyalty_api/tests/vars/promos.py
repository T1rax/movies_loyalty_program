from collections import OrderedDict

from src.api.models.promo import (
    PromoActivateResponse,
    PromoResponse,
    PromoType,
)
from src.common.repositories import queries


test_products = ["product_1", "product_2"]


async def _insert_promo(pool, test_data: dict):
    row_data = await pool.fetchrow(queries.CREATE_PROMO, *test_data.values())
    return row_data


async def create_promo(
    pool,
    campaign_name="test",
    products=None,
    type=PromoType.DISCOUNT.value,
    value=10,
    duration=None,
    activation_date=None,
    # user_ids=None,
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
        # user_ids=user_ids,
        activations_limit=activations_limit,
    )
    row_data = await _insert_promo(pool, test_data)

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
    # user_ids=None,
    activations_limit=1,
    created_dt=None,
    updated_dt=None,
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
            # "user_ids": user_ids,
            "activations_limit": activations_limit,
            "created_dt": created_dt,
            "updated_dt": updated_dt,
        },
        "errors": None,
    }


async def _insert_promo_activation(pool, test_data: dict):
    row_data = await pool.fetchrow(
        queries.CREATE_PROMO_ACTIVATION, *test_data.values()
    )
    return row_data


async def create_promo_activation(
    pool,
    promo_id=1,
    user_id="a1bee0ec-02a2-42cf-9aa6-ee82835aabaf",
    activations_cnt=1,
):
    test_data = OrderedDict(
        promo_id=promo_id,
        user_id=user_id,
        activations_cnt=activations_cnt,
    )
    row_data = await _insert_promo_activation(pool, test_data)
    print("--DAT", row_data)

    return PromoActivateResponse.parse_obj(row_data) if row_data else None
