import os

from pydantic import AmqpDsn, BaseSettings


class BaseSenderSettings(BaseSettings):
    run: bool = True
    url: AmqpDsn
    exchange: str


class CalculationOfPointsAmqpSender(BaseSenderSettings):
    pass


CALCULATION_OF_POINTS_SENDER = {
    "url": os.getenv(
        "CALCULATION_OF_POINTS_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "exchange": os.getenv(
        "CALCULATION_OF_POINTS_SENDER_EXCHANGE",
        default="points.add",
    ),
}