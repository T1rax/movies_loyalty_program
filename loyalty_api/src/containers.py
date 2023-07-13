from dependency_injector import containers, providers
from src.common.connectors import amqp, db
from src.common.repositories.loyalty import LoyaltyRepository
from src.common.services.loyalty import LoyaltyService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.api.srv.endpoints.promos", "src.api.v1.endpoints.promos"]
    )

    db_client = providers.Factory(db.DbConnector)
    amqp_client = providers.Factory(amqp.AMQPSenderPikaConnector)

    loyalty_repository = providers.Factory(LoyaltyRepository, db=db_client)

    loyalty_service = providers.Factory(
        LoyaltyService,
        repository=loyalty_repository,
    )
