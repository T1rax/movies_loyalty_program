from http import HTTPStatus
from unittest import mock

import pytest
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.auth import TEST_PUBLIC_KEY, sign_jwt
from tests.vars.promos import create_promo, get_promo_by_id

from loyalty_api.tests.vars.tables import LOYALTY_TABLES


@pytest.mark.parametrize(
    "user_ids",
    (
        ["a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"],
        [],
    ),
)
@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_deactivate_ok(
    pool, test_client, test_app, user_ids, monkeypatch
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    promo_activation_cnt = 0
    user_promo_activation = None
    body = {"promo_code": promo_code, "user_id": user_id}

    monkeypatch.setattr(
        "src.settings.auth_settings.jwt_secret", TEST_PUBLIC_KEY
    )
    test_client.cookies["access_token_cookie"] = sign_jwt(user_id=user_id)

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        user_ids=user_ids,
        promo_code=promo_code,
    )

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation_cnt.return_value = (
        promo_activation_cnt
    )
    loyalty_repository_mock.get_promo_activation.return_value = (
        user_promo_activation
    )

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/v1/promos/deactivate", json=body
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"success": True, "result": "Ok", "errors": None}


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_deactivate_user_not_found(
    pool, test_client, test_app, monkeypatch
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    user_promo_ids = ["a1bee0ec-02a2-42cf-9aa6-ee82835aaba3"]
    user_promo = None
    body = {"promo_code": promo_code, "user_id": user_id}

    monkeypatch.setattr(
        "src.settings.auth_settings.jwt_secret", TEST_PUBLIC_KEY
    )
    test_client.cookies["access_token_cookie"] = sign_jwt(user_id=user_id)

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        user_ids=user_promo_ids,
        promo_code=promo_code,
    )
    new_promo = await get_promo_by_id(pool, promo.id)

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = new_promo
    loyalty_repository_mock.get_user_promo.return_value = user_promo

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/v1/promos/deactivate", json=body
        )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "errors": ["Promo_code for user not found."],
        "result": None,
        "success": False,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_code_has_already_been_used(
    pool, test_client, test_app, monkeypatch
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    activations_limit = 1
    body = {"promo_code": promo_code, "user_id": user_id}

    monkeypatch.setattr(
        "src.settings.auth_settings.jwt_secret", TEST_PUBLIC_KEY
    )
    test_client.cookies["access_token_cookie"] = sign_jwt(user_id=user_id)

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code=promo_code,
        activations_limit=activations_limit,
    )

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation_cnt.return_value = 1

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/v1/promos/deactivate", json=body
        )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "errors": ["The promo_code has already been used."],
        "result": None,
        "success": False,
    }
