import logging
from http import HTTPStatus

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.web import HTTPException
from common.exceptions import RequestException
from common.models.requests import RequestMethod
from settings import settings


logger = logging.getLogger(__name__)


class ServiceCommunicator:
    """
    Класс для общения с другими сервисами
    """

    def __init__(self):
        self.loyalty_url = settings.loyalty_api.url
        self.default_headers = {settings.token.token: settings.token.token}

    async def send_request(
        self,
        method: RequestMethod,
        url: str,
        path: str,
        json_data: dict | None = None,
        headers: dict | None = None,
    ) -> tuple[int, dict]:
        if not json_data:
            json_data = {}
        if not headers:
            headers = {}
        if headers.keys() & self.default_headers.keys():
            raise RequestException(
                "Заголовки содержат зарезервированные параметры"
            )
        try:
            async with aiohttp.ClientSession() as session:
                if method == RequestMethod.POST:
                    async with session.post(
                        url + path,
                        json=json_data,
                        headers=self.default_headers,
                    ) as resp:
                        response_dict = await resp.json()
                        status = resp.status
                elif method == RequestMethod.GET:
                    async with session.get(
                        url + path,
                        json=json_data,
                        headers=self.default_headers,
                    ) as resp:
                        response_dict = await resp.json()
                        status = resp.status
                else:
                    raise RequestException("Неподдерживаемый метод запроса")
            return status, response_dict
        except HTTPException as ex:
            logger.exception(
                "Сетевая ошибка причина: \n $s", ex.reason, exc_info=True
            )
            raise RequestException("Ошибка отправки")
        except ClientConnectorError:
            logger.exception("Ошибка соединения", exc_info=True)
            raise RequestException("Cannot connect to api host")

    async def create_promo(self, json_data: dict) -> tuple[bool, str]:
        try:
            status, response_dict = await self.send_request(
                RequestMethod.POST,
                self.loyalty_url,
                "/api/v1/promo",
                json_data,
            )
            if status == HTTPStatus.OK:
                promo_id = response_dict.get("promo_id")
                return True, f"Промокод успешно сгенерирован, id {promo_id}"
            else:
                return False, response_dict.get("detail")  # type: ignore
        except RequestException as ex:
            return False, str(ex)
