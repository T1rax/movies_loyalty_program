import aiomisc
import click


@click.group()
def cli():
    pass


@cli.command(help="run-consumers")
@click.pass_context
def run_consumers(ctx):
    from src.workers.consumers.runner import main

    with aiomisc.entrypoint(
        *main.consumers,
        log_config=False,
        debug=main.config.debug,
    ) as loop:
        loop.run_forever()


if __name__ == "__main__":
    cli()
