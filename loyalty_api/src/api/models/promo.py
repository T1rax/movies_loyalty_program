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
    id: int
    campaign_name: str
    promo_code: str
    products: list[str]
    type: str
    value: int
    duration: int | None
    activation_date: datetime | None
    user_ids: list[str]
    activations_limit: int
    created_dt: datetime | None
    updated_dt: datetime | None


class PromoActivateInput(ORDJSONModelMixin):
    promo_code: str
    user_id: str | None
