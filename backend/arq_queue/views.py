from arq_queue.worker import job_pool


async def health_check_api():
    await job_pool.enqueue_job("health_check")
    return {"success": True}
