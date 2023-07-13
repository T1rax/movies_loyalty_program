import datetime
from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.api.models.promo import PromoType
from src.common.exceptions import DatabaseError
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import (
    create_promo,
    get_promo_by_id,
    get_promos_response,
)

from loyalty_api.tests.vars.tables import LOYALTY_TABLES


@pytest.mark.parametrize(
    """
    user_ids,
    activation_date,
    duration
    """,
    (
        (
            ["a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"],
            datetime.datetime.utcnow(),
            10,
        ),
        ([], datetime.datetime.utcnow() + datetime.timedelta(days=5), None),
    ),
)
@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_create_promo_ok(
    pool, test_client, test_app, user_ids, activation_date, duration
):
    campaign_name = "test"
    products = ["subscription_1", "subscription_2"]
    type = PromoType.DISCOUNT.value
    value = 10
    promo_code = "7J2ep6M="
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
        promo_code=promo_code,
    )
    test_client.headers[settings.token_settings.token_header] = "test"
    loyalty_service_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_service_mock.create_promo.return_value = promo
    with test_app.container.loyalty_service.override(loyalty_service_mock):
        response = await test_client.post("/api/srv/v1/promos", json=body)

    new_promo = await get_promo_by_id(pool, promo.id)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == get_promos_response(**new_promo.dict())


@pytest.mark.parametrize(
    "token, status",
    (
        ("", HTTPStatus.UNAUTHORIZED),
        ("fake_token", HTTPStatus.FORBIDDEN),
    ),
)
async def test_create_promo_token_error(test_client, token, status):
    body = {
        "campaign_name": "test",
        "products": ["subscription_1", "subscription_2"],
        "type": PromoType.DISCOUNT.value,
        "value": 3,
    }
    test_client.headers[settings.token_settings.token_header] = token

    response = await test_client.post("/api/srv/v1/promos", json=body)
    assert response.status_code == status


@pytest.mark.xfail(raises=DatabaseError)
async def test_create_promo_error_500(test_client):
    body = {
        "campaign_name": "test",
        "products": ["subscription_1", "subscription_2"],
        "type": PromoType.DISCOUNT.value,
        "value": 3,
    }
    test_client.headers[settings.token_settings.token_header] = "test"

    response = await test_client.post("/api/srv/v1/promos", json=body)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
