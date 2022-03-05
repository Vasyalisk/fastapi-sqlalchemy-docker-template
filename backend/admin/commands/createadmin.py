import typer

from admin.main import admin_datastore, app
from admin.database import database as db


def command(
        email: str,
        password: str
):
    with app.app_context():
        admin_datastore.create_user(email=email, password=password)
        db.session.commit()

    typer.echo("Admin is created successfully.")
