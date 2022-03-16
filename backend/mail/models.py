import sqlalchemy as orm

from database import models
from database import mixins


class Mail(models.BaseTable, mixins.ModelMixin):
    from_email = orm.Column(orm.String(length=320))
    to_emails = orm.Column(orm.ARRAY(orm.String(length=320)))

    sent_at = orm.Column(orm.DateTime, default=None, nullable=True)
    content_text = orm.Column(orm.Text)
    content_html = orm.Column(orm.Text)
