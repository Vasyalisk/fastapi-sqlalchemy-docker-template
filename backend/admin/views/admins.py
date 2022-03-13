from flask_admin.contrib.sqla import ModelView

from admin.views.mixins import AuthorizedAdminMixin


class AdminUserView(AuthorizedAdminMixin, ModelView):
    can_delete = True
    can_create = True
