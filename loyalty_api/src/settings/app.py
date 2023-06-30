from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class AppSettings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)

    project_host: str = Field(env="LA_APP_HOST", default="0.0.0.0")
    project_port: int = Field(env="LA_APP_PORT", default=8006)

    log_format: str = Field(env="LOG_FORMAT", default="INFO")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings = AppSettings()
