import logging
from collections import defaultdict

from src.common.clients.amqp_sender import AMQPSenderPika
from src.common.connectors.amqp import AMQPSenderPikaConnector


logger = logging.getLogger(__name__)


class MockAMQPSender(AMQPSenderPika):
    def __init__(self, *args, **kwargs):
        super().__init__(settings={})
        self.cache = defaultdict(list)

    async def send(self, message, exchange=None, **kwargs):
        await self.__call__(message, exchange, **kwargs)

    async def __call__(self, message, exchange, **kwargs):
        logger.warning(
            f"{self.__class__.__name__} send message {message} {kwargs}"
        )
        self.cache[exchange].append(message)


class MockAMQPSenderPikaConnector(AMQPSenderPikaConnector):
    amqp_sender: AMQPSenderPika = None

    def __init__(self, config: dict):
        super().__init__(config={})
        self._settings = config
        self.amqp_sender = MockAMQPSender(settings=self._settings)
