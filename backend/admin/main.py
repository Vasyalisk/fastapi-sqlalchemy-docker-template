from flask import Flask
from flask_admin.menu import MenuLink

from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin

from admin.database import database as db
from admin import models as admin_models
from admin import views
from admin.config import settings
from admin.routers import connect_routers

from users import models as user_models

app = Flask("Admin")
connect_routers(app)
app.config.from_object(settings)

db.init_app(app)
admin_datastore = SQLAlchemyUserDatastore(
    db,
    user_model=admin_models.AdminUser,
    role_model=admin_models.Role
)
security_app = Security(app, admin_datastore)
admin_app = Admin(
    app,
    url="/admin",
    template_mode='bootstrap4',
    name=settings.PROJECT_NAME,
    index_view=views.AuthorizedAdminIndexView(url="/", endpoint="/")
)
admin_app.url_with_root = "/admin"

admin_app.add_view(
    views.AdminUserView(admin_models.AdminUser, db.session, name="Administrators", category="Users")
)
admin_app.add_view(
    views.UserView(user_models.User, db.session, name="Users", category="Users")
)

admin_app.add_link(
    MenuLink(name="Logout", category="", endpoint="logout")
)
