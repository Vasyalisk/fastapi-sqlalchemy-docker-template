from arq_queue.worker import worker


async def health_check_api():
    await worker.enqueue_job("health_check")
    return {"success": True}
