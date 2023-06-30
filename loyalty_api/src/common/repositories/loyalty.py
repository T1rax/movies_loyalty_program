import logging

from src.common.connectors.db import DbConnector


logger = logging.getLogger(__name__)


class LoyaltyRepository:
    def __init__(self, db: DbConnector):
        self._db = db
