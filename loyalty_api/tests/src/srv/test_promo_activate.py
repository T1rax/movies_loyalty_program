from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.common.promo import get_promo_code
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import create_promo

from loyalty_api.tests.vars.tables import LOYALTY_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_activate_ok(pool, test_client, test_app):
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    promo_code = get_promo_code()
    body = {"promo_code": promo_code, "user_id": user_id}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        # user_ids=[user_id],
        promo_code=promo_code,
    )
    # promo_activation = await create_promo_activation(pool, promo_id=promo.id, user_id=user_id)
    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation_cnt.return_value = 0
    loyalty_repository_mock.get_promo_activation.return_value = None

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/activate", json=body
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"success": True, "result": "Ok", "errors": None}
