from http import HTTPStatus
from unittest import mock

import pytest
from src import settings
from src.common.repositories.loyalty import LoyaltyRepository
from tests.vars.promos import (
    create_promo,
    get_promo_by_id,
    get_promos_response,
)

from loyalty_api.tests.vars.tables import LOYALTY_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_get_promo_info_ok(pool, test_client, test_app):
    promo_code = "7J2ep6M="

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
        response = await test_client.get(
            f"/api/srv/v1/promos/{promo_code}",
        )
    new_promo = await get_promo_by_id(pool, promo.id)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == get_promos_response(**new_promo.dict())


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [LOYALTY_TABLES], indirect=True)
async def test_get_promo_info_not_found(pool, test_client, test_app):
    promo_code = "7J2ep6M="

    await create_promo(
        pool,
        campaign_name="test_campaign",
        promo_code=promo_code,
    )
    test_client.headers[settings.token_settings.token_header] = "test"

    loyalty_repository_mock = mock.AsyncMock(spec=LoyaltyRepository)
    loyalty_repository_mock.get_promo_by_promo_code.return_value = None

    with test_app.container.loyalty_repository.override(
        loyalty_repository_mock
    ):
        response = await test_client.get(
            "/api/srv/v1/promos/fE724qp=",
        )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "errors": ["Сouldn't find a promo with this promo_code."],
        "result": None,
        "success": False,
    }
