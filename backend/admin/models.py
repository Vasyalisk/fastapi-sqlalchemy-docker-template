from flask_security import RoleMixin, UserMixin

import sqlalchemy as orm
from sqlalchemy.orm import relationship

from database.models import BaseTable
from database.mixins import ModelMixin, PrimaryKeyMixin
from admin.database import database as db


class Role(BaseTable, ModelMixin, RoleMixin):
    query = db.session.query_property()

    name = orm.Column(orm.String(80), unique=True)
    description = orm.Column(orm.String(255))

    admins = relationship("AdminUser", secondary="admin_role", back_populates="roles")


class AdminUser(BaseTable, ModelMixin, UserMixin):
    query = db.session.query_property()

    email = orm.Column(orm.String(255), unique=True)
    password = orm.Column(orm.String(255))
    active = orm.Column(orm.Boolean(), default=True)
    confirmed_at = orm.Column(orm.DateTime())

    roles = relationship('Role', secondary="admin_role", back_populates='admins')


class AdminRole(BaseTable, PrimaryKeyMixin):
    query = db.session.query_property()

    admin_id = orm.Column(orm.Integer(), orm.ForeignKey("admin_user.id", ondelete="CASCADE"))
    role_id = orm.Column(orm.Integer(), orm.ForeignKey("role.id", ondelete="CASCADE"))
