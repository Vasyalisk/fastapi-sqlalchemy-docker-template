import asyncio

from arq import cron, ArqRedis
from arq.jobs import Job

from typing import Union, Iterable


async def health_check(ctx: dict):
    print("Arq health check done...")


async def composite_job(ctx: dict, workflow: tuple[Union[Iterable[dict], dict]]):
    """
    Enqueues and executes jobs in the background in the given order / flow

    Usage:

    await job_pool.enqueue_job(
        "composite_job",
        (
            {
                "name": "foo_job_name",
                "args": <iterable of args passed to foo_job_name job>,
                "kwargs": <dict of kwargs passed to foo_job_name job>,
                "immutable": True <whether to ignore result of previous job as input or not, defaults to True>
            },

            # Jobs in the tuple will be executed in parallel
            (
                {
                    "name": "bar_job_name",
                    "immutable": False # Will take result of foo_job_name as input
                },
                {
                    "name": "baz_job_name",
                    "immutable": False # Will take result of foo_job_name as input
                }
            ),
            {
                "name": "iterable_job",
                "immutable": False # Will take iterable of bar_job_name and baz_job_name results as input
            }
        )
    )
    :param ctx:
    :param workflow: tuple of dict / tuples
    :return: result of the final job in the workflow
    """
    intermediate_result = None
    for job_payload in workflow:
        try:
            intermediate_result = await parallel_job(
                ctx=ctx,
                *job_payload,
                intermediate_result=intermediate_result
            )
            intermediate_result = [await one.result() for one in intermediate_result]
        except TypeError:
            intermediate_result = await intermediate_job(
                ctx=ctx,
                job_payload=job_payload,
                intermediate_result=intermediate_result
            )
            intermediate_result = await intermediate_result.result()
    return intermediate_result


async def intermediate_job(
        ctx: dict,
        job_payload: dict,
        intermediate_result=None
) -> Job:
    """
    Used in conjunction with composite_job

    Enqueues job with given payload and returns Job which can be turned into proper result
    :param ctx:
    :param job_payload:
    :param intermediate_result:
    :return:
    """
    job_pool: ArqRedis = ctx["redis"]
    is_immutable: bool = job_payload.get("immutable")
    kwargs: dict = job_payload.pop("kwargs", {})
    args: list = job_payload.pop("args", [])
    name: str = job_payload.pop("name")

    if not is_immutable and intermediate_result is not None:
        try:
            kwargs.update(**intermediate_result)
        except TypeError:
            pass
        try:
            args.extend(*intermediate_result)
        except TypeError:
            args.append(intermediate_result)

    intermediate_result = await job_pool.enqueue_job(name, *args, **kwargs)
    return intermediate_result


async def parallel_job(
        ctx: dict,
        *job_payloads: dict,
        intermediate_result=None
) -> Iterable[Job]:
    """
    Used in conjunction with composite_job

    Enqueues jobs with given payloads in parallel and returns iterable of Jobs
    :param ctx:
    :param job_payloads:
    :param intermediate_result:
    :return:
    """
    jobs = []
    for single_payload in job_payloads:
        jobs.append(intermediate_job(
            ctx=ctx,
            job_payload=single_payload,
            intermediate_result=intermediate_result
        ))
    intermediate_result = await asyncio.gather(*jobs)
    return intermediate_result


functions = [
    health_check,
    composite_job,
]

cron_jobs = [
    # cron(
    #     health_check,
    #     name="health-check-each-minute",
    #     minute={*range(60)}
    # )
]
