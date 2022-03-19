import typer
import os

from mail.config import settings


def command(template_name: str):
    html_path = f"{settings.EMAIL_TEMPLATES_PATH}html/{template_name}.html"
    text_path = f"{settings.EMAIL_TEMPLATES_PATH}text/{template_name}.txt"

    html_exists = os.path.exists(html_path)
    if html_exists:
        typer.echo(".html template already exists!")
        return

    text_exists = os.path.exists(html_path)
    if text_exists:
        typer.echo(".txt template already exists!")
        return

    open(html_path, "w+").close()
    open(text_path, "w+").close()

    os.chmod(path=html_path, mode=0o777)
    os.chmod(path=text_path, mode=0o777)

    typer.echo("Templates are successfully created!")
