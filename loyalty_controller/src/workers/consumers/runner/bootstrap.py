import punq
from settings.consumers import ConsumersConfig
from src.common.clients.loyalty_api import (
    LoyaltyApiClient,
    resolve_loyalty_api_client,
)
from src.common.connectors.amqp import (
    AMQPSenderPikaConnector,
    resolve_amqp_sender_client,
)
from src.workers.consumers.calculation_of_points.consumer import (
    CalculationOfPointsConsumer,
)
from src.workers.consumers.calculation_of_points.service import (
    CalculationOfPointsService,
)


def resolve_resources(config: ConsumersConfig) -> punq.Container:
    container = punq.Container()

    container.register(
        service=AMQPSenderPikaConnector,
        instance=resolve_amqp_sender_client(
            config=config.calculation_of_points_amqp_sender
        ),
    )

    container.register(
        service=LoyaltyApiClient,
        instance=resolve_loyalty_api_client(config=config.loyalty_api_client),
    )
    container.register(service=CalculationOfPointsService)
    container.register(
        service=CalculationOfPointsConsumer,
        factory=CalculationOfPointsConsumer,
        config=config.calculation_of_points_consumer,
    )

    return container
