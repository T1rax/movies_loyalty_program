import logging
from http import HTTPStatus

from pydantic import ValidationError
from src.common.clients.loyalty_api import LoyaltyApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.exceptions import BadRequestError, ClientError, ServiceError
from src.workers.models.loyalty_card import LoyaltyCardInfo, DepositPointsModel


logger = logging.getLogger(__name__)


class DepositPointsService:
    def __init__(
        self,
        loyalty_api_client: LoyaltyApiClient,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._loyalty_api_client = loyalty_api_client
        self._amqp_sender = amqp_sender

    async def main(self, body: bytes) -> None:
        deposit_event = self._load_model(body)
        user_id, points = deposit_event.user_id, deposit_event.points

        user_card_info = await self.get_user_card_info(user_id)
        if not user_card_info:
            logger.info(
                "Loyalty card was not found for the user: user_id %s",
                user_id,
            )
            return

        await self.deposit_points(user_id, points)

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

    async def deposit_points(self, user_id: str, points: int) -> None:
        try:
            response_status = await self._loyalty_api_client.refill_card(
                user_id, points
            )
            if response_status != HTTPStatus.OK:
                logger.warning(
                    "Received error trying deposit points: user_id %s, http_code %s",
                    user_id,
                    response_status
                )
        except (BadRequestError, ServiceError, ClientError):
            logger.warning(
                "Getting user card info error: user_id %s",
                user_id,
                exc_info=True,
            )

    @staticmethod
    def _load_model(  # type: ignore
        body: bytes,
    ) -> DepositPointsModel | None:
        try:
            return DepositPointsModel.parse_raw(body)
        except ValidationError:
            logger.warning(
                "Fail to parse data for deposit event - %s",
                body,
                exc_info=True,
            )
