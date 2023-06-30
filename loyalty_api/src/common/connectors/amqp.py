from src.common.clients.amqp_sender import AMQPSenderPika
from src.settings import loyalty_amqp_settings


class AMQPSenderPikaConnector:
    amqp_sender: AMQPSenderPika | None = None

    @classmethod
    async def setup(cls):
        cls.amqp_sender = AMQPSenderPika(settings=loyalty_amqp_settings.dict())
        await cls.amqp_sender.setup()

    @classmethod
    async def close(cls):
        if cls.amqp_sender:
            await cls.amqp_sender.close()
            cls.amqp_sender = None
