import logging

import aiomisc
from src.common.base_consumer import BaseRunner
from src.common.clients.loyalty_api import LoyaltyApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.workers.consumers.calculation_of_points.consumer import (
    CalculationOfPointsConsumer,
)
from src.workers.consumers.deposit_points.consumer import DepositPointsConsumer


logger = logging.getLogger(__name__)


class Runner(BaseRunner):
    def __init__(
        self,
        amqp_sender: AMQPSenderPikaConnector,
        loyalty_api_client: LoyaltyApiClient,
        calculation_of_points_consumer: CalculationOfPointsConsumer,
        deposit_points_consumer: DepositPointsConsumer,
    ):
        self._amqp_sender = amqp_sender
        self._loyalty_api_client = loyalty_api_client
        self._calculation_of_points_consumer = calculation_of_points_consumer
        self._deposit_points_consumer = deposit_points_consumer

    @property
    def consumers(self):
        self._setup()
        return self._resolve_consumer_list()

    @property
    def clients(self):
        return self._resolve_client_list()

    def _setup(self):
        @aiomisc.receiver(aiomisc.entrypoint.PRE_START)
        async def startup(entrypoint, services):
            await self._amqp_sender.setup()

            for consumer in self.consumers:
                await consumer.startup()

            logger.info("Server started")

        @aiomisc.receiver(aiomisc.entrypoint.POST_STOP)
        async def shutdown(entrypoint):
            await self._amqp_sender.close()

            for consumer in self.consumers:
                await consumer.shutdown()

            for client in self.clients:
                await client.close()
