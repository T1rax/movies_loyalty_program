import os
import socket

from pydantic import AmqpDsn, BaseSettings, PositiveInt

from settings import LoyaltyApiSettings, CalculationOfPointsAmqpSender
from settings.base import BaseConfig


class BaseConsumerSettings(BaseSettings):
    run: bool = True
    consumer_tag: str
    url: AmqpDsn
    queue_name: str
    exchange_name: str
    routing_key: str
    prefetch_count: PositiveInt = 5
    timeout: PositiveInt = 5


class CalculationOfPointsConfig(BaseConfig):
    # клиенты
    loyalty_api_client: LoyaltyApiSettings
    calculation_of_points_amqp_sender: CalculationOfPointsAmqpSender
    # консьюмеры
    calculation_of_points_consumer: BaseConsumerSettings


class ConsumersConfig(CalculationOfPointsConfig):
    pass


CONSUMER_TAG = (
    os.getenv("TASK_CONSUMER_TAG", default=None) or socket.gethostname()
)


CALCULATION_OF_POINTS_CONSUMER = {
    "url": os.getenv(
        "CALCULATION_OF_POINTS_CONSUMER_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "queue_name": os.getenv(
        "CALCULATION_OF_POINTS_CONSUMER_QUEUE",
        default="calculation_of_points.payment",
    ),
    "exchange_name": os.getenv(
        "CALCULATION_OF_POINTS_CONSUMER_EXCHANGE",
        default="calculation_of_points.payment",
    ),
    "routing_key": os.getenv(
        "CALCULATION_OF_POINTS_CONSUMER_ROUTING_KEY",
        default="event.payment",
    ),
    "consumer_tag": CONSUMER_TAG,
}