from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8007)


class DatabaseSettings(BaseSettings):
    url: str = Field(
        env="DATABASE_URL",
        default="postgresql://app:123qwe@db:5432/loyalty",
    )
    name: str = Field(env="POSTGRES_DB", default="loyalty")


class TokenSettings(BaseSettings):
    header: str = Field(
        env="TOKEN_HEADER",
        default="X-AUTH-TOKEN",
    )
    token: str = Field(env="LOYALTY_ADMIN_SRV_TOKEN", default="test")


class LoyaltyApiSettings(BaseSettings):
    host: str = Field(env="LA_APP_HOST", default="0.0.0.0")
    port: int = Field(env="LA_APP_PORT", default=8006)
    url: str = Field(env="LA_APP__URL", default="https://0.0.0.0:8006")


class AdminPanelSettings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)
    log_format: str = Field(env="LOG_FORMAT", default="INFO")
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    token: TokenSettings = TokenSettings()
    loyalty_api: LoyaltyApiSettings = LoyaltyApiSettings()

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        env_nested_delimiter = "__"
        env_prefix = "LADMIN_"  # Loyalty Admin Panel


settings = AdminPanelSettings()
