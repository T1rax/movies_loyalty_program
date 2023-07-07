import logging
from typing import Optional

import jwt
from dotenv import load_dotenv
from fastapi import Cookie
from src.settings import auth_settings


load_dotenv()

logger = logging.getLogger(__name__)


def get_decoded_data(
    token: Optional[str] = Cookie(None, alias=auth_settings.auth_secure_key)
) -> Optional[dict]:
    if not token:
        return None

    try:
        decoded_token = jwt.decode(
            token,
            auth_settings.jwt_secret,
            algorithms=[auth_settings.jwt_algorithm],
        )
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        logger.error("Invalid token or expired signature.", exc_info=True)
        return None
    return decoded_token
