from src.common.clients.amqp_sender import AMQPSenderPika


class AMQPSenderPikaConnector:
    amqp_sender: AMQPSenderPika | None = None

    def __init__(self, config: dict):
        self._settings = config

    async def setup(self):
        self.amqp_sender = AMQPSenderPika(settings=self._settings.dict())
        await self.amqp_sender.setup()

    @classmethod
    async def close(cls):
        if cls.amqp_sender:
            await cls.amqp_sender.close()
            cls.amqp_sender = None


def resolve_amqp_sender_client(config: dict):
    return AMQPSenderPikaConnector(config=config)
