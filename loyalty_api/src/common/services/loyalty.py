import logging

from src.common.repositories.loyalty import LoyaltyRepository


logger = logging.getLogger(__name__)


class LoyaltyService:
    def __init__(
        self,
        repository: LoyaltyRepository,
    ):
        self._repository = repository
