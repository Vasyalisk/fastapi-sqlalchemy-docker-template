from flask_security import logout_user
from flask import redirect, url_for, request, Flask


def connect_routers(app: Flask):
    app.add_url_rule("/logout", view_func=logout, methods=["get"])


def logout():
    logout_user()
    return redirect(url_for("/.index", next=request.url))
