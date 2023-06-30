from pydantic import AmqpDsn, BaseSettings, Field


class LoyaltyAmqpSender(BaseSettings):
    url: AmqpDsn = Field(
        env="LOYALTY_SENDER_AMQP_URL",
        default="amqp://user:pass@127.0.0.1:8030/test",
    )
    exchange: str = Field(
        env="LOYALTY__SENDER_EXCHANGE",
        default="loyalty",
    )
    routing_key: str = Field(
        env="LOYALTY_SENDER_ROUTING_KEY", default="event.*"
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


loyalty_amqp_settings = LoyaltyAmqpSender()
