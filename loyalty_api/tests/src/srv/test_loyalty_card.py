from http import HTTPStatus

import pytest
from tests.fake.repository import FakeLoyaltyRepository


async def test_create_card(test_api_client, test_app):
    with test_app.container.loyalty_repository.override(
        FakeLoyaltyRepository()
    ):
        response = test_api_client.post(
            "api/srv/loyalty_cards", json={"user_id": "test_create_uuid"}
        )

    assert response.status_code == HTTPStatus.OK

    response_dict = response.json()
    assert response_dict["result"]["id"] == "loyalty_id_12345"


@pytest.mark.parametrize(
    "action, level, response_status, result_level",
    [
        ("exact", 10, HTTPStatus.OK, 10),
        ("exact", 9, HTTPStatus.BAD_REQUEST, None),
        ("up", None, HTTPStatus.OK, 10),
        ("down", None, HTTPStatus.BAD_REQUEST, None),
    ],
)
async def test_change_loyalty_level(
    test_api_client, test_app, action, level, response_status, result_level
):
    with test_app.container.loyalty_repository.override(
        FakeLoyaltyRepository()
    ):
        response = test_api_client.post(
            "api/srv/loyalty_cards/change_level",
            json={
                "user_id": "test_uuid",
                "action": action,
                "loyalty_level": level,
            },
        )

    assert response.status_code == response_status

    if response.status_code == HTTPStatus.OK:
        response_dict = response.json()
        assert response_dict["result"]["loyalty_level"] == result_level


async def test_get_card_info(test_api_client, test_app):
    with test_app.container.loyalty_repository.override(
        FakeLoyaltyRepository()
    ):
        response = test_api_client.get(
            "api/srv/loyalty_cards/test_uuid",
        )

    assert response.status_code == HTTPStatus.OK

    response_dict = response.json()
    assert response_dict["result"]["loyalty_id"] == "loyalty_id_12345"


async def test_get_card_balance_history(test_api_client, test_app):
    with test_app.container.loyalty_repository.override(
        FakeLoyaltyRepository()
    ):
        response = test_api_client.get(
            "api/srv/loyalty_cards/history/test_uuid",
        )

    assert response.status_code == HTTPStatus.OK

    response_dict = response.json()
    assert type(response_dict["result"]) == list
    assert type(response_dict["result"][0]["points"]) == int


async def test_loyalty_card_refill(test_api_client, test_app):
    with test_app.container.loyalty_repository.override(
        FakeLoyaltyRepository()
    ):
        response = test_api_client.post(
            "api/srv/loyalty_cards/refill",
            json={"user_id": "test_uuid", "points": 100, "source": "test"},
        )

    assert response.status_code == HTTPStatus.OK

    response_dict = response.json()
    assert response_dict["result"] == "success"


async def test_loyalty_card_deduct(test_api_client, test_app):
    with test_app.container.loyalty_repository.override(
        FakeLoyaltyRepository()
    ):
        response = test_api_client.post(
            "api/srv/loyalty_cards/deduct",
            json={"user_id": "test_uuid", "points": 100, "source": "test"},
        )

    assert response.status_code == HTTPStatus.OK

    response_dict = response.json()
    assert response_dict["result"] == "success"
