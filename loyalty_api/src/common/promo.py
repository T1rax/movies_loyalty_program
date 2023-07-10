import base64
import os

from src import settings


def get_promo_code() -> str:
    code = os.urandom(settings.LENGTH_CODE)
    promo_code = base64.b64encode(code)
    return promo_code.decode("utf-8")
