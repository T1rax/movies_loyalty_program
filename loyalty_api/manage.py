import click
from src.settings import logger, settings


@click.group()
def cli():
    pass


@cli.command("api")
def api():
    import uvicorn
    from src.app import create_app

    uvicorn.run(
        create_app(),
        host=settings.project_host,
        port=settings.project_port,
        log_config=logger.LOGGING,
    )


if __name__ == "__main__":
    cli()
