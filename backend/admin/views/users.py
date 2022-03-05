from flask_admin.contrib.sqla import ModelView

from admin.views.mixins import AuthorizedAdminView


class UserView(AuthorizedAdminView, ModelView):
    can_create = True
    can_delete = True
