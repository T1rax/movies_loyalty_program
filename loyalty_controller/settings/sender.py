from pydantic import AmqpDsn, BaseSettings


class BaseSenderSettings(BaseSettings):
    run: bool = True
    url: AmqpDsn
    exchange: str
