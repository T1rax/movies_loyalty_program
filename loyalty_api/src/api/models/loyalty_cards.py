from datetime import datetime
from enum import Enum

from src.api.models.base import ORDJSONModelMixin


class LoyaltyCardResponse(ORDJSONModelMixin):
    id: str
    user_id: str
    loyalty_level: int
    created_dt: datetime | None
    updated_dt: datetime | None


class LoyaltyCardBalanceResponse(ORDJSONModelMixin):
    loyalty_id: str
    user_id: str
    balance: int


class LoyaltyCardBalanceHistoryResponse(ORDJSONModelMixin):
    id: str
    points: int
    source: str
    created_dt: datetime


class LoyaltyCardFullInfoResponse(ORDJSONModelMixin):
    loyalty_id: str
    user_id: str
    loyalty_level: int
    balance: int
    created_dt: datetime | None
    updated_dt: datetime | None


class LoyaltyCardInput(ORDJSONModelMixin):
    user_id: str


class LoyaltyCardLevelActions(str, Enum):
    # Повышение на следующий уровень
    UP = "up"
    # Понизить на 1 уровень ниже
    DOWN = "down"
    # укзаать определенный уровень лояльности
    EXACT = "exact"


class ChangeLoyaltyCardLevelInput(ORDJSONModelMixin):
    user_id: str | None = None
    action: LoyaltyCardLevelActions = LoyaltyCardLevelActions.EXACT
    loyalty_level: int | None = None


class PointsLoyaltyCardInput(ORDJSONModelMixin):
    loyalty_id: str | None = None
    user_id: str | None = None
    points: int
    source: str = "undefined"
