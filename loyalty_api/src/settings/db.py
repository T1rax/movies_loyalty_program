from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class DBSettings(BaseSettings):
    db_url: str = Field(
        env="DATABASE_URL",
        default="postgresql://app:123qwe@localhost:6668/loyalty",
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


db_settings = DBSettings()
