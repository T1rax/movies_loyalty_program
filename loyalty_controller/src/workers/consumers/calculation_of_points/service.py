import logging

from pydantic import ValidationError
from src.common.clients.loyalty_api import LoyaltyApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.exceptions import BadRequestError, ClientError, ServiceError
from src.common.utils import calculate_percentages
from src.workers.models.loyalty_card import LoyaltyCardInfo, PaymentEventModel


logger = logging.getLogger(__name__)


class CalculationOfPointsService:
    def __init__(
        self,
        loyalty_api_client: LoyaltyApiClient,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._loyalty_api_client = loyalty_api_client
        self._amqp_sender = amqp_sender

    async def main(self, body: bytes) -> None:
        payment_event = self._load_model(body)
        user_id, amount = payment_event.user_id, payment_event.amount

        user_card_info = await self.get_user_card_info(user_id)
        if not user_card_info:
            return

        loyalty_level = user_card_info.loyalty_level
        points = calculate_percentages(loyalty_level, amount)
        await self.send_message(user_id, points)

    async def get_user_card_info(self, user_id: str) -> LoyaltyCardInfo | None:
        try:
            user_card_info = await self._loyalty_api_client.get_card_info(
                user_id
            )
        except (BadRequestError, ServiceError, ClientError):
            logger.warning(
                "Getting user card info error: user_id %s",
                user_id,
                exc_info=True,
            )
            return  # type: ignore
        return LoyaltyCardInfo(**user_card_info) if user_card_info else None

    async def send_message(self, user_id: str, points: int) -> None:
        message = {
            "user_id": user_id,
            "points": points,
        }
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
