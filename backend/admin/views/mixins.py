from flask_security import current_user
from flask import url_for, request, redirect


class AuthorizedAdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))
