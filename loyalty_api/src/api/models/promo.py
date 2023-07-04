from datetime import datetime
from enum import Enum

from src.api.models.base import ORDJSONModelMixin


class PromoType(str, Enum):
    # скидка в %
    DISCOUNT = "discount"
    # скидка в рублях
    NOMINAL = "nominal"
    # баллы лояльности
    POINTS = "points"


class PromoInput(ORDJSONModelMixin):
    campaign_name: str
    products: set[str]
    type: PromoType
    value: int
    duration: int | None
    activation_date: datetime | None
    user_ids: set[str] | None = set()
    activations_limit: int = 1


class PromoResponse(ORDJSONModelMixin):
    promo_id: int
    campaign_name: str
    promo_code: str
    products: list[str]
    type: str
    value: int
    duration: int | None
    activation_date: datetime | None
    user_ids: list
    activations_limit: int
