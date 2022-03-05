import typer

from subprocess import Popen
import os

APP_CONTENT = {
    "__init__.py": "",
    "models.py": "",
    "crud.py": "from {app_name} import models\n",
    "schemas.py": "from pydantic import BaseModel\n",
    "views.py": "",
    "serializers.py": "",
    "routers.py": (
        "from core.routers import ViewAPIRouter\n"
        "\n"
        "router = ViewAPIRouter(prefix='/{app_name}', tags=[\"{app_name}\"])"
    ),
}


def command(app_name: str = typer.Argument(...)):
    app_exists = os.path.exists(app_name)

    if app_exists:
        typer.echo(f"{app_name} already exists!")
        return

    context = {
        "app_name": app_name
    }

    os.mkdir(app_name)
    for file_name, content in APP_CONTENT.items():
        content = content.format(**context)
        with open(f"{app_name}/{file_name}", "w+") as file:
            file.write(content)

    Popen(["chmod", "-R", "777", app_name])
    typer.echo(f"Successfully created {app_name} app")
