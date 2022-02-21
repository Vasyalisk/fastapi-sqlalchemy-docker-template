import sqlalchemy as orm

from database import models
from database import mixins


class User(models.BaseTable, mixins.ModelMixin):
    username = orm.Column(orm.String(length=255), nullable=False, unique=True)
    password = orm.Column(orm.String(length=255), nullable=False)

    def __repr__(self):
        return self.username
