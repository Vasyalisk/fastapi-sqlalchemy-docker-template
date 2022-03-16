from arq import cron


async def health_check(ctx: dict):
    print("Arq health check done...")


functions = [
    health_check
]

cron_jobs = [
    cron(
        health_check,
        name="health-check-each-minute",
        minute={*range(60)}
    )
]
