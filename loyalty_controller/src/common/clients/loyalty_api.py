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

    @staticmethod
    async def is_json_successful(status) -> bool:
        return status in (200, 201)

    async def get_card_info(self, user_id: str) -> dict | None:
        """Получить информацию по карте лояльности."""

        url = f"/api/srv/loyalty_cards/{user_id}"
        response_body = await self.get(url=url, headers=self.default_headers)
        if await self.is_json_successful(response_body.status_code):
            response = response_body.json()
            return dpath.get(response, "result", default=None)  # type: ignore
        else:
            return None

    async def refill_card(self, user_id: str, points: int) -> int:
        """Пополнить счет карты лояльности."""

        url = "/api/srv/loyalty_cards/refill"
        parameters = {
            "user_id": user_id,
            "points": points,
            "source": "deposit_points_worker",
        }
        response = await self.post(
            url=url,
            headers=self.default_headers,
            json=parameters,
        )
        return response.status_code


def resolve_loyalty_api_client(config: LoyaltyApiSettings):
    return LoyaltyApiClient(
        base_url=config.url,
        token=config.token,
    )
