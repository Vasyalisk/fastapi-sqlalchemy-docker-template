import sqlalchemy as orm

from users import models
from database.utils import with_session, AsyncSession


@with_session()
async def get_user_or_none(session: AsyncSession = None, **kwargs) -> models.User:
    query = orm.select(models.User).filter_by(**kwargs)
    model = await session.scalar(query)
    return model
