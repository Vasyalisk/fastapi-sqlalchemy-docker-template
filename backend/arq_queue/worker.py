from arq import create_pool, ArqRedis
from arq.constants import default_queue_name

from arq_queue.config import WorkerSettings


# noinspection PyAbstractClass
class ArqWorker(ArqRedis):
    # noinspection PyShadowingNames
    async def create_pool(
            self,
            *,
            retry: int = 0,
            job_serializer=None,
            job_deserializer=None,
            default_queue_name: str = default_queue_name
    ):
        new_pool = await create_pool(
            settings_=WorkerSettings.redis_settings,
            retry=retry,
            job_serializer=job_serializer,
            job_deserializer=job_deserializer,
            default_queue_name=default_queue_name
        )
        self.job_deserializer = new_pool.job_deserializer
        self.job_serializer = new_pool.job_serializer
        self.default_queue_name = new_pool.default_queue_name
        self._pool_or_conn = new_pool._pool_or_conn


# Task orchestration docs
# https://github.com/samuelcolvin/arq/issues/245
job_pool = ArqWorker(None)
