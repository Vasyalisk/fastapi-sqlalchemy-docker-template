from flask_admin.contrib.sqla import ModelView

from admin.views.mixins import AuthorizedAdminMixin


class UserView(AuthorizedAdminMixin, ModelView):
    can_create = True
    can_delete = True
