from flask_admin import AdminIndexView

from admin.views.mixins import AuthorizedAdminView


class AuthorizedAdminIndexView(AuthorizedAdminView, AdminIndexView):
    def is_visible(self):
        return False
