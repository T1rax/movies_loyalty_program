from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import (
    create_promo,
    create_promo_activation,
    get_promo_activation,
    get_promo_by_id,
)

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
async def test_get_promo_status_ok(
    pool,
    test_client,
    test_app,
    user_ids,
    fastapi_limiter,
    flush_redis,
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    promo_activation_cnt = 0
    user_promo_activation = None
    body = {"promo_code": promo_code, "user_id": user_id}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        user_ids=user_ids,
        promo_code=promo_code,
    )
    user_promo = await get_promo_by_id(pool, promo.id)

    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation_cnt.return_value = (
        promo_activation_cnt
    )
    loyalty_repository_mock.get_user_promo.return_value = user_promo
    loyalty_repository_mock.get_promo_activation.return_value = (
        user_promo_activation
    )

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/status", json=body
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"success": True, "result": "Ok", "errors": None}

    user_promo_activation = await get_promo_activation(pool, promo.id, user_id)
    assert user_promo_activation is None


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_get_promo_status_not_found(
    pool, test_client, test_app, fastapi_limiter, flush_redis
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
    new_promo = await get_promo_by_id(pool, promo.id)

    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = new_promo
    loyalty_repository_mock.get_user_promo.return_value = user_promo

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/status", json=body
        )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "errors": ["Promo_code for user not found."],
        "result": None,
        "success": False,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_get_promo_status_limit_has_been_reached(
    pool, test_client, test_app, fastapi_limiter, flush_redis
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    activations_limit = 2
    body = {"promo_code": promo_code, "user_id": user_id}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code=promo_code,
        activations_limit=activations_limit,
    )

    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation_cnt.return_value = (
        activations_limit
    )

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/status", json=body
        )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "errors": ["Activation limit has been reached."],
        "result": None,
        "success": False,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_get_promo_status_user_has_already_activated(
    pool, test_client, test_app, fastapi_limiter, flush_redis
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    activations_limit = 2
    body = {"promo_code": promo_code, "user_id": user_id}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code=promo_code,
        activations_limit=activations_limit,
    )

    promo_activations = await create_promo_activation(
        pool,
        promo_id=promo.id,
        user_id=user_id,
    )

    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo
    loyalty_repository_mock.get_promo_activation_cnt.return_value = 1
    loyalty_repository_mock.get_promo_activation.return_value = (
        promo_activations
    )

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/status", json=body
        )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "errors": ["User has already activated promo."],
        "result": None,
        "success": False,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_get_promo_status_too_many_requests(
    pool, test_client, test_app, fastapi_limiter, flush_redis
):
    promo_code = "7J2ep6M="
    user_id = "a1bee0ec-02a2-42cf-9aa6-ee82835aabaf"
    body = {"promo_code": promo_code, "user_id": user_id}

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)

    test_client.headers[settings.token_settings.token_header] = "test"

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        for i in range(20):
            response = await test_client.post(
                "/api/srv/v1/promos/status", json=body
            )
            assert response.status_code == HTTPStatus.NOT_FOUND
            assert response.json() == {
                "errors": ["Сouldn't find a promo with this promo_code."],
                "result": None,
                "success": False,
            }

        response = await test_client.post(
            "/api/srv/v1/promos/status", json=body
        )
        assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
        assert response.json() == {
            "errors": ["Too Many Requests"],
            "result": None,
            "success": False,
        }
