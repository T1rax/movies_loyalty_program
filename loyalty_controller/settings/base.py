from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_nested_delimiter = "__"
        use_enum_values = True

    debug: bool = False
