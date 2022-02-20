from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import AsyncSessionLocal


async def get_async_session() -> AsyncSession:
    """
    Example usage:
     in API:
        session: db.AsyncSession = Depends(db.get_async_session)
     executing query:
        import sqlalchemy as orm
        query = orm.select(MyModel)
        result = await session.execute(query)
        see https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
    :return:
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


def with_session(session_name="session"):
    """
    Decorator to pass db.AsyncSession in case where FastAPI injection can't be used. Closes session after function
    execution
    Usage:
        @db.with_session()
        async def foo(session: db.AsyncSession):
            # do_stuff
            await session.commit()
    :param session_name: optional kwarg name which will be injected into decorated function, defaults to "session"
    :return:
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with AsyncSessionLocal() as session:
                kwargs[session_name] = session
                return await func(*args, **kwargs)

        return wrapper

    return decorator
