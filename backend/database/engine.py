from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from database.session import AsyncSession
from config import settings


class SessionMaker(sessionmaker):
    def __call__(self, **local_kw) -> AsyncSession:
        return super().__call__(**local_kw)


async_engine = create_async_engine(
    settings.database_url, echo=settings.ECHO_SQL,
)

AsyncSessionLocal = SessionMaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)
