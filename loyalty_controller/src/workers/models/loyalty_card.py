from pydantic import BaseModel


class PaymentEventModel(BaseModel):
    user_id: str
    amount: int


class LoyaltyCardInfo(BaseModel):
    user_id: str
    loyalty_level: int
