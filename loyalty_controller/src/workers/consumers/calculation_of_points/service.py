import logging

import dpath
from pydantic import BaseModel, ValidationError

from src.common.clients.loyalty_api import LoyaltyApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector


logger = logging.getLogger(__name__)


class PaymentEventModel(BaseModel):
    user_id: str
    amount: int


class CalculationOfPointsService:
    def __init__(
        self,
        loyalty_api_client: LoyaltyApiClient,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._loyalty_api_client = loyalty_api_client
        self._amqp_sender = amqp_sender

    async def main(self, body: bytes) -> None:
        pass

    async def send_message(self, message: dict) -> None:
        # {
        #     "user_id": message.user_id,
        #     "points": message.points,
        # }
        try:
            await self._amqp_sender.amqp_sender.send(  # type: ignore
                message=message,
                routing_key="event.add",
            )
        except Exception:
            logger.exception(
                "Fail to send message: message %s",
                message,
                exc_info=True,
            )

    @staticmethod
    def _load_model(  # type: ignore
        body: bytes,
    ) -> PaymentEventModel | None:
        try:
            return PaymentEventModel.parse_raw(body)
        except ValidationError:
            logger.warning(
                "Fail to parse data for payment event - %s",
                body,
                exc_info=True,
            )
