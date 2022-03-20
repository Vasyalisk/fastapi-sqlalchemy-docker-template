from aioredis import Redis, create_redis_pool

from redis_db.config import settings


# noinspection PyAbstractClass
class RedisClient(Redis):
    ENCODING = "utf-8"

    async def create_pool(self):
        new_pool = await create_redis_pool(
            settings.redis_url,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_APP_DB,
        )
        # noinspection PyProtectedMember
        self._pool_or_conn = new_pool._pool_or_conn


redis_client = RedisClient(None)
