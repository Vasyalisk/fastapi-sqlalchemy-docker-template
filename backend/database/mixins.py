from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as orm

from uuid import uuid4


class PrimaryKeyMixin:
    id = orm.Column(orm.Integer, primary_key=True)


class UidMixin:
    uid = orm.Column(UUID(as_uuid=True), unique=True, default=uuid4)


class CreatedAtMixin:
    created_at = orm.Column(orm.DateTime, server_default=orm.text("NOW()"))


class UpdatedAtMixin:
    updated_at = orm.Column(orm.DateTime, server_default=orm.text("NOW()"), onupdate=orm.text("NOW()"))


class ModelMixin(PrimaryKeyMixin, UidMixin, CreatedAtMixin, UpdatedAtMixin):
    pass
