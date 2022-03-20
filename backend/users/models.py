import sqlalchemy as orm

from database import models
from database import mixins


class User(models.BaseTable, mixins.ModelMixin):
    email = orm.Column(orm.String(length=320), nullable=False, unique=True)
    password = orm.Column(orm.String(length=255), nullable=False)
    is_email_verified = orm.Column(orm.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self.username
