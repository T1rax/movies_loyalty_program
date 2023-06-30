import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class TokenSettings(BaseSettings):
    token_header: str = Field(
        env="TOKEN_HEADER",
        default="X-AUTH-TOKEN",
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


token_settings = TokenSettings()

TEST_TOKEN = "test"
UGC_SRV_TOKEN = os.getenv("UGC_SRV_TOKEN", default=TEST_TOKEN)
ADMIN_PANEL_SRV_TOKEN = os.getenv("ADMIN_PANEL_SRV_TOKEN", default=TEST_TOKEN)

LOYALTY_SRV_TOKENS = {
    UGC_SRV_TOKEN,
    ADMIN_PANEL_SRV_TOKEN,
}
