import secrets

import typer

SECRET_KEY_LENGTH = 32


def command() -> str:
    api_key = secrets.token_urlsafe(SECRET_KEY_LENGTH)
    typer.echo(api_key)
    return api_key
