from datetime import datetime

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

    async def get_card_info(self, user_id: str) -> dict:
        """Получить информацию по карте лояльности."""

        url = f"/loyalty_cards/{user_id}"
        params = {"user_id": user_id}
        response_body = await self.get(
            url=url, headers=self.default_headers, params=params
        )
        response = response_body.json()
        # return dpath.get(response, "result", default=None)  # type: ignore
        return dict(
            loyalty_id="loyalty_id_12345",
            user_id=user_id,
            loyalty_level=5,
            balance=100,
            created_dt=datetime.now(),
            updated_dt=datetime.now(),
        )


def resolve_loyalty_api_client(config: LoyaltyApiSettings):
    return LoyaltyApiClient(
        base_url=config.url,
        token=config.token,
    )
