from pydantic import AnyHttpUrl, BaseSettings


class BaseClientSettings(BaseSettings):
    url: AnyHttpUrl
