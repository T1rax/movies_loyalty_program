import string

import humanhash
from src import settings


SYMBOLS = string.ascii_letters + string.digits + "!#$%&-_"


def get_promo_code() -> str:
    return humanhash.humanize(SYMBOLS, words=settings.NUMBER_OF_WORDS)
