from collections import OrderedDict

from src.api.models.promo import PromoResponse, PromoType
from src.common.repositories import queries


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
    user_ids=None,
    activations_limit=1,
    promo_code=None,
):
    test_data = OrderedDict(
        campaign_name=campaign_name,
        promo_code=promo_code,
        products=products,
        type=type,
        value=value,
        duration=duration,
        activation_date=activation_date,
        user_ids=user_ids,
        activations_limit=activations_limit,
    )
    row_data = await _insert_promo(pool, test_data)

    return PromoResponse.parse_obj(row_data) if row_data else None


def get_promos_response(
    promo_id=1,
    campaign_name="test",
    promo_code=None,
    products=None,
    type=None,
    value=None,
    duration=None,
    activation_date=None,
    user_ids=None,
    activations_limit=1,
):
    if activation_date:
        activation_date = activation_date.isoformat()
    return {
        "success": True,
        "result": {
            "promo_id": promo_id,
            "campaign_name": campaign_name,
            "promo_code": promo_code,
            "products": products,
            "type": type,
            "value": value,
            "duration": duration,
            "activation_date": activation_date,
            "user_ids": user_ids,
            "activations_limit": activations_limit,
        },
        "errors": None,
    }
