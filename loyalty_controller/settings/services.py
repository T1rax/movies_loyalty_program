import os

from pydantic import AnyHttpUrl, BaseSettings


class BaseClientSettings(BaseSettings):
    url: AnyHttpUrl


class LoyaltyApiSettings(BaseClientSettings):
    token: str


LOYALTY_API_SERVICE = {
    "url": os.getenv("LOYALTY_API_SERVICE", default="http://0.0.0.0:8000"),
    "token": os.getenv(
        "LOYALTY_API_SRV_TOKEN",
        default="test",
    ),
}
