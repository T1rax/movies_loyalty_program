import datetime
from http import HTTPStatus
from unittest import mock

import pytest
from src.api.models.promo import PromoType
from src.common.promo import get_promo_code
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import create_promo, get_promos_response

from loyalty_api.tests.vars.tables import LOYALTY_TABLES


@pytest.mark.parametrize(
    """
    user_ids,
    activation_date
    """,
    (
        (["a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"], datetime.datetime.utcnow()),
        ([], datetime.datetime.utcnow() + datetime.timedelta(days=5)),
    ),
)
@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_create_promo_ok(
    pool, test_client, test_app, user_ids, activation_date
):
    campaign_name = "test"
    products = ["subscription_1", "subscription_2"]
    type = PromoType.DISCOUNT.value
    value = 10
    duration = 10
    promo_code = get_promo_code()
    body = {
        "campaign_name": campaign_name,
        "products": products,
        "type": type,
        "value": value,
        "duration": duration,
        "activation_date": activation_date.isoformat(),
        "user_ids": user_ids,
        "activations_limit": 1,
    }

    promo = await create_promo(
        pool,
        campaign_name=campaign_name,
        activation_date=activation_date,
        products=products,
        type=type,
        value=value,
        duration=duration,
        user_ids=user_ids,
        promo_code=promo_code,
    )
    test_client.headers["X-AUTH-TOKEN"] = "test"
    loyalty_service_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_service_mock.create_promo.return_value = promo
    with test_app.container.loyalty_service.override(loyalty_service_mock):
        response = await test_client.post("/api/srv/v1/promos", json=body)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == get_promos_response(**promo.dict())
