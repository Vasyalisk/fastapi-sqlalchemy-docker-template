import typer
import alembic.config

from typing import Optional
from migrations import utils


@utils.with_alembic_workdir
def command(
        name: Optional[str] = typer.Argument(None),
        empty: Optional[bool] = typer.Option(False, "--empty")
):
    if name is None:
        name = "auto"

    argv = ["revision", "--autogenerate", "-m", name]
    if empty:
        argv.pop(1)
    alembic.config.main(argv=argv)

