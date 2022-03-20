import sqlalchemy as orm

from database.utils import with_session
from database.session import AsyncSession

from users import models


@with_session()
async def get_user_by_username(username, session: AsyncSession = None) -> models.User:
    query = orm.select(models.User).where(
        models.User.username == username
    )
    model = await session.scalar(query)
    return model


@with_session()
async def get_user(session: AsyncSession = None, **kwargs) -> models.User:
    query = orm.select(models.User).filter_by(
        **kwargs
    )
    model = await session.scalar(query)
    return model


@with_session()
async def get_user_by_id(user_id, session: AsyncSession = None) -> models.User:
    query = orm.select(models.User).where(
        models.User.id == user_id
    )
    model = await session.scalar(query)
    return model


@with_session()
async def register_user(session: AsyncSession = None, **kwargs) -> models.User:
    model = models.User(**kwargs)
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model
