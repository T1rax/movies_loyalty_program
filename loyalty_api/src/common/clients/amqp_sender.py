import abc
import asyncio
import logging

import aio_pika
import ujson
from aio_pika import Message


logger = logging.getLogger(__name__)


ROBUST_TIMEOUT = 60
DEFAULT_RECONNECT_DELAY = 5


class AMQPBase(metaclass=abc.ABCMeta):
    """
    Базовый класс для клентов получения/отправки в очередь сообщений
    """

    def __init__(self, settings: dict):
        self._settings = settings

    @abc.abstractmethod
    async def setup(self):
        """
        Старт работы клиента
        """

    @abc.abstractmethod
    async def shutdown(self):
        """
        Ожидание завершения событий
        """

    async def close(self):
        """
        Завершение  работы клиента
        """
        try:
            await self.shutdown()
        except Exception as e:
            logger.exception("Error %s shutdown, error: %s", self, e)


class AMQPSenderPika(AMQPBase):
    def __init__(
        self,
        settings: dict,
        reconnect_on_errors: bool = True,
    ):
        self.reconnect_on_errors = reconnect_on_errors

        self._reconnect_delay = settings.pop(
            "reconnect_delay", DEFAULT_RECONNECT_DELAY
        )

        super().__init__(settings)

        self.exchange = settings.get("exchange")
        self._connection: aio_pika.connection.Connection | None = None
        self._channel: aio_pika.channel.Channel | None = None
        self._is_alive = False
        self.robust_timeout = settings.get("robust_timeout") or ROBUST_TIMEOUT
        self.exchanges: dict[str, aio_pika.Exchange] = dict()

    async def _connect(self):
        try_num = 0

        while True:
            try:
                self._connection = await aio_pika.connect_robust(
                    **self._settings, timeout=self.robust_timeout
                )
                self._channel = await self._connection.channel()
                logger.info("Pika amqp connected")
                self._is_alive = True

                break
            except aio_pika.exceptions.ConnectionClosed:
                logger.warning("Pika ConnectionClosed, will call on_error")
            except OSError as e:
                if not self.reconnect_on_errors:
                    raise e
                logger.error(
                    "Cannot connect Pika to AMQP. Try connect %s after %s sec",
                    try_num + 1,
                    self._reconnect_delay,
                )

            await asyncio.sleep(self._reconnect_delay)
            try_num += 1

    async def setup(self):
        logger.info("Init Pika amqp sender")
        await self._connect()

    async def shutdown(self):
        logger.info("Calling Pika shutdown")

        if self._connection is not None:
            try:
                await self._connection.close()
            except aio_pika.exceptions.ConnectionClosed:
                pass

        if self._channel is not None:
            try:
                await self._channel.close()
            except aio_pika.exceptions.ChannelClosed:
                pass

        self._channel, self._connection = None, None

    async def get_exchange(self, exchange: str) -> aio_pika.Exchange:
        if exchange not in self.exchanges:
            rmq_exchange = await self._channel.get_exchange(name=exchange)
            self.exchanges[exchange] = rmq_exchange
        else:
            rmq_exchange = self.exchanges[exchange]
        return rmq_exchange

    async def _send(
        self, message: dict, exchange: str = "", routing_key: str = ""
    ):
        if not self._channel.is_closed:
            message = ujson.dumps(message)
            encoded_message = Message(str(message).encode())
            rmq_exchange = await self.get_exchange(exchange)
            await rmq_exchange.publish(
                encoded_message, routing_key=routing_key
            )
        else:
            logger.info(
                "Waiting for opening pika channel for sending message..."
            )
            await self.setup()
            await self._send(message, exchange, routing_key)

    async def send(self, message, routing_key, exchange=None, *args, **kwargs):
        exchange = exchange if exchange else self.exchange
        await self.__call__(message, exchange, routing_key, *args, **kwargs)

    async def __call__(self, message, exchange, routing_key, *args, **kwargs):
        await self._send(message, exchange, routing_key, *args, **kwargs)
