from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import (
    create_promo,
    create_promo_activation,
    delete_user_promo_activation,
    get_promo_activation,
)
from tests.vars.tables import LOYALTY_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_restore_ok(pool, test_client, test_app):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    body = {"promo_code": promo_code, "user_id": user_id}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        user_ids=[user_id],
        promo_code=promo_code,
    )
    promo_activations = await create_promo_activation(
        pool,
        promo_id=promo.id,
        user_id=user_id,
    )

    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation.return_value = (
        promo_activations
    )
    loyalty_repository_mock.delete_user_promo_activation.return_value = (
        await delete_user_promo_activation(pool, promo.id, user_id)
    )

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/restore", json=body
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"success": True, "result": "Ok", "errors": None}

    user_promo_activation = await get_promo_activation(pool, promo.id, user_id)
    assert user_promo_activation is None
