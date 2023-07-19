from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import create_promo, set_flag_deactivated_promo

from loyalty_api.tests.vars.tables import LOYALTY_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_deactivate_ok(pool, test_client, test_app):
    promo_code = "7J2ep6M="
    body = {"promo_code": promo_code}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code=promo_code,
    )
    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = promo

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/deactivate", json=body
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"success": True, "result": "Ok", "errors": None}


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_deactivate_not_found(pool, test_client, test_app):
    body = {"promo_code": "6G1st8K="}

    await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code="7J2ep6M=",
    )
    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = None

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/deactivate", json=body
        )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "errors": ["Сouldn't find a promo with this promo_code."],
        "result": None,
        "success": False,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_promo_deactivate_already_deactivated(
    pool, test_client, test_app
):
    promo_code = "7J2ep6M="
    body = {"promo_code": promo_code}

    promo = await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code=promo_code,
    )
    await set_flag_deactivated_promo(pool, promo.id, True)
    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.post(
            "/api/srv/v1/promos/deactivate", json=body
        )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "errors": ["The promo_code has already been deactivated."],
        "result": None,
        "success": False,
    }
