from datetime import datetime
from enum import Enum

from pydantic import Field
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
    products: list[str]
    type: PromoType
    value: int
    duration: int | None
    activation_date: datetime = Field(default_factory=datetime.now())
    user_id: str | None
    activations_limit: int = Field(default_factory=1)
