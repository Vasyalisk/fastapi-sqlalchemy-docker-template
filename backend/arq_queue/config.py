from arq.connections import RedisSettings

from config import settings
from arq_queue.utils import detect_jobs

detected_tasks, detected_cron_jobs = detect_jobs()


class WorkerSettings:
    functions = detected_tasks

    cron_jobs = detected_cron_jobs

    on_startup = None
    on_shutdown = None

    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        database=settings.REDIS_ARQ_DB,
        password=settings.REDIS_PASSWORD
    )
