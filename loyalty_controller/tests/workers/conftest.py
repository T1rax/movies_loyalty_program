import re
from datetime import datetime
from http import HTTPStatus

import punq
import pytest
import respx
from src.common.clients.loyalty_api import LoyaltyApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.workers.consumers.calculation_of_points.service import (
    CalculationOfPointsService,
)
from src.workers.consumers.deposit_points.service import DepositPointsService
from tests.utils.amqp import MockAMQPSenderPikaConnector


@pytest.fixture
async def resolve_amqp_sender_connector():
    return MockAMQPSenderPikaConnector(config={})


@pytest.fixture
async def test_loyalty_api_client():
    client = LoyaltyApiClient(base_url="http://0.0.0.0/", token="test")
    yield client


@pytest.fixture
def calculation_of_points_service(
    test_loyalty_api_client, resolve_amqp_sender_connector
) -> CalculationOfPointsService:
    container = punq.Container()

    container.register(
        service=LoyaltyApiClient,
        instance=test_loyalty_api_client,
    )
    container.register(
        service=AMQPSenderPikaConnector, instance=resolve_amqp_sender_connector
    )

    container.register(service=CalculationOfPointsService)

    yield container.resolve(CalculationOfPointsService)


@pytest.fixture
def deposit_points_service(
    test_loyalty_api_client, resolve_amqp_sender_connector
) -> CalculationOfPointsService:
    container = punq.Container()

    container.register(
        service=LoyaltyApiClient,
        instance=test_loyalty_api_client,
    )
    container.register(
        service=AMQPSenderPikaConnector, instance=resolve_amqp_sender_connector
    )

    container.register(service=DepositPointsService)

    yield container.resolve(DepositPointsService)


@pytest.fixture
def mock_external_services():
    with respx.mock(base_url="http://0.0.0.0/") as respx_mock:
        yield respx_mock


@pytest.fixture
async def mock_loyalty_api_ok(mock_external_services):
    resp = {
        "result": dict(
            loyalty_id="f51f3683-0000-402e-9cf4-785f840d0000",
            user_id="f51f3683-7758-402e-9cf4-785f840d8738",
            loyalty_level=5,
            balance=100,
            created_dt=datetime.now().isoformat(),
            updated_dt=datetime.now().isoformat(),
        )
    }
    mock_external_services.get(
        re.compile(".*/api/srv/loyalty_cards.*")
    ).respond(
        json=resp,
        status_code=HTTPStatus.OK,
    )

    refill_resp = {"result": "success"}
    mock_external_services.post(
        re.compile(".*/api/srv/loyalty_cards/refill.*")
    ).respond(
        json=refill_resp,
        status_code=HTTPStatus.OK,
    )
