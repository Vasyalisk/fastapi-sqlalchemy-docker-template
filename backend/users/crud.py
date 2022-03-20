import sqlalchemy as orm

from database.utils import with_session, AsyncSession
from users import models as user_models


@with_session()
async def get_one_by_id(user_id, session: AsyncSession = None) -> user_models.User:
    query = orm.select(user_models.User).where(
        user_models.User.id == user_id
    )
    result = await session.scalar(query)
    return result
