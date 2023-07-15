from http import HTTPStatus
from unittest import mock

import pytest
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.auth import TEST_PUBLIC_KEY, sign_jwt
from tests.vars.promos import (
    create_promo,
    create_promo_activation,
    delete_user_promo_activation,
    get_promo_activation,
)
from tests.vars.tables import LOYALTY_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_restore_ok(pool, test_client, test_app, monkeypatch):
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

    monkeypatch.setattr(
        "src.settings.auth_settings.jwt_secret", TEST_PUBLIC_KEY
    )
    test_client.cookies["access_token_cookie"] = sign_jwt(user_id=user_id)

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
        response = await test_client.post("/api/v1/promos/restore", json=body)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"success": True, "result": "Ok", "errors": None}

    user_promo_activation = await get_promo_activation(pool, promo.id, user_id)
    assert user_promo_activation is None


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_restore_user_not_found(
    pool, test_client, test_app, monkeypatch
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    user_promo_ids = ["a1bee0ec-02a2-42cf-9aa6-ee82835aaba3"]
    user_promo = None
    body = {"promo_code": promo_code, "user_id": user_id}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        user_ids=user_promo_ids,
        promo_code=promo_code,
    )
    monkeypatch.setattr(
        "src.settings.auth_settings.jwt_secret", TEST_PUBLIC_KEY
    )
    test_client.cookies["access_token_cookie"] = sign_jwt(user_id=user_id)

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation.return_value = user_promo

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post("/api/v1/promos/restore", json=body)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "errors": ["User did not activate this promo_code."],
        "result": None,
        "success": False,
    }
