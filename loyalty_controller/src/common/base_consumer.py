import abc
import logging

import aio_pika
import aiomisc
from httpx import AsyncClient
from settings.consumers import BaseConsumerSettings


logger = logging.getLogger(__name__)


class BaseConsumer(aiomisc.Service):
    def __init__(self, config: BaseConsumerSettings):
        super().__init__()
        self._config = config
        self._connection: aio_pika.RobustConnection = None  # type: ignore
        self._channel: aio_pika.RobustChannel = None  # type: ignore
        self._queue: aio_pika.RobustQueue = None  # type: ignore

    @property
    def consumer(self):
        if not self._config.run:
            return None
        return self

    async def start(self):
        self.start_event.set()
        logger.info(
            "%s service start to consume messages.", self.__class__.__name__
        )
        await self._queue.consume(
            self._process_message, consumer_tag=self._config.consumer_tag
        )

    async def stop(self, exception: Exception = None):  # type: ignore
        await self._queue.cancel(consumer_tag=self._config.consumer_tag)
        logger.info(
            "%s service stop to consume messages.", self.__class__.__name__
        )

    async def startup(self):
        if self.consumer is None:
            return
        self._connection = await aio_pika.connect_robust(
            url=self._config.url, timeout=self._config.timeout
        )

        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=self._config.prefetch_count)

        self._queue = await self._channel.declare_queue(
            name=self._config.queue_name,
            durable=True,
            timeout=self._config.timeout,
        )
        await self._make_queue_bindings()
        logger.info("%s connection is established.", self.__class__.__name__)

    async def shutdown(self):
        if self.consumer is None:
            return
        await self._channel.close()
        await self._connection.close()
        logger.info("%s connection is closed.", self.__class__.__name__)

    @abc.abstractmethod
    async def _process_message(
        self, message: aio_pika.abc.AbstractIncomingMessage
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def _make_queue_bindings(self):
        raise NotImplementedError


class BaseRunner:
    def _resolve_consumer_list(self) -> list[BaseConsumer]:
        return [
            value
            for value in self.__dict__.values()
            if isinstance(value, BaseConsumer) and value.consumer is not None
        ]

    def _resolve_client_list(self) -> list[AsyncClient]:
        return [
            value
            for value in self.__dict__.values()
            if isinstance(value, AsyncClient)
        ]
