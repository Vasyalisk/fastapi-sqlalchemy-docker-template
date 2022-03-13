from flask_admin import AdminIndexView

from admin.views.mixins import AuthorizedAdminMixin


class AuthorizedAdminIndexView(AuthorizedAdminMixin, AdminIndexView):
    def is_visible(self):
        return False
