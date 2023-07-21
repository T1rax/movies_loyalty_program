import dpath
from httpx import AsyncClient
from settings.services import LoyaltyApiSettings


class LoyaltyApiClient(AsyncClient):
    def __init__(
        self,
        base_url: str,
        token: str,
    ):
        super().__init__(base_url=base_url)
        self.token = token

    @property
    def default_headers(self) -> dict:
        return {"X-Token": self.token}


def resolve_loyalty_api_client(config: LoyaltyApiSettings):
    return LoyaltyApiClient(
        base_url=config.url,
        token=config.token,
    )
