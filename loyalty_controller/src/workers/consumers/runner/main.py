from settings import ConsumersConfig
from src.workers.consumers.runner import application, bootstrap


config = ConsumersConfig()

resources = bootstrap.resolve_resources(config=config)

resources.register(application.Runner)

consumers = resources.resolve(application.Runner).consumers
