from enum import Enum

# from pydantic import BaseModel, Field


class PromoType(str, Enum):
    # деньги
    MONEY = "money"
    # скидка в процентах
    DISCOUNT = "discount"
    # баллы
    POINTS = "points"
