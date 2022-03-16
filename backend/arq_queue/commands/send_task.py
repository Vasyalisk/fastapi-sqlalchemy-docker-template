import typer
import asyncio

from arq_queue.worker import worker


def command(
        task_name: str,
        wait_for_result: bool = typer.Option(False, "--wait", "-w")
):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_runner(
        task_name=task_name,
        wait_for_result=wait_for_result
    ))


async def _runner(
        task_name: str,
        wait_for_result: bool = False
):
    if worker._pool_or_conn is None:
        await worker.create_pool()

    job = await worker.enqueue_job(task_name)
    typer.echo(f"Task {task_name} is sent!")

    if not wait_for_result:
        return

    typer.echo("Waiting for result...")
    result = await job.result()

    try:
        msg = str(result)
    except Exception:
        msg = result.__repr__()

    typer.echo(msg)
    typer.echo("Task is done!")
