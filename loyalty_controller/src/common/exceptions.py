import httpx


class ClientError(Exception):
    """Бросает ошибку при системных проблемах с запросом"""

    def __init__(
        self,
        message: str,
        request: httpx.Request,
        parent_exception: type[httpx.RequestError],
    ):
        super().__init__(message)
        self.request = request
        self.parent_exception = parent_exception


class ResponseError(Exception):
    """Бросает ошибку при некорректных кодах ответа"""

    def __init__(
        self, message: str, request: httpx.Request, response: httpx.Response
    ):
        super().__init__(message)
        self.request = request
        self.response = response


class BadRequestError(ResponseError):
    """Бросает ошибку для 4хх кодов ответа"""


class ServiceError(ResponseError):
    """Бросает ошибку для 5хх кодов ответа"""
