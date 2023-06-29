import json
import logging

import aio_pika
import backoff
from aio_pika import DeliveryMode, Message
from aio_pika.exceptions import AMQPConnectionError


logger = logging.getLogger(__name__)


class RabbitMQ:
    def __init__(
        self,
        host: str,
        port: int,
        virtualhost: str,
        login: str,
        password: str,
        queue: str,
    ):
        self.host = host
        self.port = port
        self.virtualhost = virtualhost
        self.login = login
        self.password = password
        self.queue = queue

    @backoff.on_exception(backoff.expo, AMQPConnectionError)
    async def get_connection(self):
        return await aio_pika.connect_robust(
            f"amqp://{self.login}:{self.password}@{self.host}:{self.port}/{self.virtualhost}",
        )

    async def send(self, message):
        connection = await self.get_connection()
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(self.queue, durable=True)
            await channel.default_exchange.publish(
                Message(
                    json.dumps(message).encode("utf-8"),
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=self.queue,
            )
            logger.info("Channel %s: Sent %s" % (channel, message))
