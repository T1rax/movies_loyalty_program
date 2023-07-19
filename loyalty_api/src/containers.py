from dependency_injector import containers, providers
from src.common.connectors import amqp, db, redis
from src.common.repositories.loyalty import LoyaltyRepository
from src.common.services.promos import PromosService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.api.srv.endpoints.promos", "src.api.v1.endpoints.promos"]
    )

    db_client = providers.Factory(db.DbConnector)
    amqp_client = providers.Factory(amqp.AMQPSenderPikaConnector)
    redis_client = providers.Factory(redis.RedisConnector)

    loyalty_repository = providers.Factory(LoyaltyRepository, db=db_client)

    promos_service = providers.Factory(
        PromosService,
        repository=loyalty_repository,
    )
