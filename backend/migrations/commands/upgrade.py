import typer
import alembic.config

from migrations import utils


@utils.with_alembic_workdir
def command(
        target: str = typer.Argument("head")
):
    argv = ["upgrade", target]
    alembic.config.main(argv=argv)
