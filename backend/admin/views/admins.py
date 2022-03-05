from flask_admin.contrib.sqla import ModelView

from admin.views.mixins import AuthorizedAdminView


class AdminUserView(AuthorizedAdminView, ModelView):
    can_delete = True
    can_create = True
