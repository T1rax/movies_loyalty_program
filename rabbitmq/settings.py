from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class RabbitMQSettings(BaseSettings):
    host: str = Field(env="RABBITMQ_HOST", default="0.0.0.0")
    port: int = Field(env="RABBITMQ_PORT", default=5672)
    virtualhost: str = Field(env="RABBITMQ_VIRTUALHOST", default="test")
    login: str = Field(env="RABBITMQ_LOGIN", default="user")
    password: str = Field(env="RABBITMQ_PASS", default="pass")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings = RabbitMQSettings()
