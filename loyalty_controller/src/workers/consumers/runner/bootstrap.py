import punq
from settings.consumers import ConsumersConfig
from src.common.connectors.amqp import (
    AMQPSenderPikaConnector,
    resolve_amqp_sender_client,
)


def resolve_resources(config: ConsumersConfig) -> punq.Container:
    container = punq.Container()

    container.register(
        service=AMQPSenderPikaConnector,
        instance=resolve_amqp_sender_client(config=config.url),
    )

    return container
