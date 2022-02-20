from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession as BaseAsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult, ScalarResult
from sqlalchemy import util

from typing import Union


class AsyncSession(BaseAsyncSession):
    """
    Async session with custom functionality
    """

    async def execute(
            self,
            statement,
            params=None,
            execution_options=util.EMPTY_DICT,
            bind_arguments=None,
            **kw
    ) -> Union[ChunkedIteratorResult, CursorResult]:
        return await super().execute(
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            **kw
        )

    async def scalars(
            self,
            statement,
            params=None,
            execution_options=util.EMPTY_DICT,
            bind_arguments=None,
            **kw
    ) -> ScalarResult:
        return await super().scalars(
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            **kw
        )
