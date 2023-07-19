from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class RedisSettings(BaseSettings):
    redis_host: str = Field(env="REDIS_HOST", default="127.0.0.1")
    redis_port: int = Field(env="REDIS_PORT", default=6379)

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


redis_settings = RedisSettings()
