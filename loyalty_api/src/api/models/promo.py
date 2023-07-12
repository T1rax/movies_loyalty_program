from datetime import datetime
from enum import Enum
from uuid import UUID

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
    activations_limit: int | None
    created_dt: datetime | None
    updated_dt: datetime | None
    linked_to_user: bool


class PromoActivateInput(ORDJSONModelMixin):
    promo_code: str


class PromoActivateInputSrv(PromoActivateInput):
    user_id: str


class PromoActivateResponse(ORDJSONModelMixin):
    id: int
    promo_id: int
    user_id: UUID
    activations_cnt: int
    created_dt: datetime | None
    updated_dt: datetime | None
