import sqlalchemy as orm

from database.utils import with_session, AsyncSession


@with_session
async def get_or_none(
        model_class,
        session: AsyncSession = None,
        **kwargs
):
    query = orm.select(model_class).filter_by(**kwargs)
    result = await session.scalar(query)
    return result


@with_session
async def update(
        model,
        session: AsyncSession = None,
        **kwargs
):
    model_class = model.__class__
    query = orm.update(
        model_class
    ).where(
        model_class.id == model.id
    ).values(
        **kwargs
    )
    result = await session.execute(query)
    await session.commit()

    if result.rowcount:
        session.add(model)
        await session.refresh(model, attribute_names=list(kwargs.keys()))

    return model


@with_session
async def create(
        model_class,
        session: AsyncSession = None,
        **kwargs
):
    model = model_class(**kwargs)
    session.add(model)
    await session.commit()
    return model


@with_session
async def delete(
        model,
        session: AsyncSession = None
):
    model_class = model.__class__
    query = orm.delete(model_class).where(model_class.id == model.id)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount
