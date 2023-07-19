from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.api.models.promo import PromoType
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import (
    create_promo,
    create_promo_activation,
    get_promo_usage_history_by_promo_ids,
)
from tests.vars.tables import LOYALTY_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_filtering_promo_usage_history(pool, test_client, test_app):
    campaign_name = "test"
    products = ["subscription_1", "subscription_2"]
    type = PromoType.DISCOUNT.value
    value = 10
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"

    promo = await create_promo(
        pool,
        campaign_name=campaign_name,
        products=products,
        type=type,
        value=value,
        promo_code=promo_code,
    )
    promo_activations = await create_promo_activation(
        pool,
        promo_id=promo.id,
        user_id=user_id,
    )
    param = {"promo_id": promo.id}
    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_usage_history_by_promo_ids.return_value = await get_promo_usage_history_by_promo_ids(
        pool, [promo.id]
    )

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.get(
            "/api/srv/v1/promos/history", params=param
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json()
