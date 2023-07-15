from enum import Enum


class RequestMethod(str, Enum):
    # почта
    GET = "get"
    POST = "post"
