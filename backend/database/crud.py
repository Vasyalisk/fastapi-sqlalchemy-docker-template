from typing import Iterable, Optional

from database.models import BaseTable
from database.engine import AsyncSession

from database.utils import with_session

import sqlalchemy as orm


class BaseCrud:
    table: BaseTable = None

    @classmethod
    @with_session()
    async def get_many(cls, model_ids, session: AsyncSession = None) -> Iterable[BaseTable]:
        query = orm.select(
            cls.table
        ).where(
            cls.table.id.in_(model_ids)
        )
        result = await session.scalars(query)
        return result

    @classmethod
    @with_session()
    async def get_or_none(cls, model_id, session: AsyncSession = None) -> Optional[BaseTable]:
        query = orm.select(
            cls.table
        ).where(
            cls.table.id == model_id
        )
        result = await session.scalar(query)
        return result

    @classmethod
    @with_session()
    async def update(cls, model_ids, session: AsyncSession = None, **kwargs) -> int:
        query = orm.update(
            cls.table
        ).where(
            cls.table.id.in_(model_ids)
        ).values(
            **kwargs
        )
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

    @classmethod
    @with_session()
    async def delete(cls, model_ids, session: AsyncSession = None) -> int:
        query = orm.delete(
            cls.table
        ).where(
            cls.table.id.in_(model_ids)
        )
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

    @classmethod
    @with_session()
    async def create(cls, session: AsyncSession = None, **kwargs):
        model = cls.table(**kwargs)
        session.add(model)
        await session.commit()
        await session.refresh(model)
        return model
