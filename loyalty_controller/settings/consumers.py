import os
import socket

from pydantic import AmqpDsn, BaseSettings, PositiveInt
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


class ConsumersConfig(BaseConfig):
    pass


CONSUMER_TAG = (
    os.getenv("TASK_CONSUMER_TAG", default=None) or socket.gethostname()
)
