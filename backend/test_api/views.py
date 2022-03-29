from mail import utils
from arq_queue import job_pool
from test_api import schemas


async def send_test_email_view(
        post_data: schemas.SendTestEmailRequest
):
    text = "Test email."
    html = "<html><p>Test email.</p></html>"
    subject = "Test email"

    is_sent = await utils.send_email(
        text=text,
        html=html,
        subject=subject,
        to_emails=post_data.to_emails
    )
    return schemas.SendTestEmailResponse(is_sent=is_sent)


async def health_check_view():
    await job_pool.enqueue_job("health_check")
    return schemas.BoolResponse()


async def composite_task_view(
        chained_msg: str = "Chained message",
        individual_msg: str = "Individual message",
):
    """
    - prints chained_msg once

    - then prints in parallel chained_msg and individual_msg

    - finally prints default message
    """
    test_workflow = (
        {
            "name": "health_check",
            "kwargs": {"msg": chained_msg}
        },
        (
            {
                "name": "health_check",
                "immutable": False
            },
            {
                "name": "health_check",
                "kwargs": {"msg": individual_msg}
            }
        ),
        {
            "name": "health_check"
        }
    )

    await job_pool.enqueue_job(
        "composite_job",
        workflow=test_workflow
    )
    return schemas.BoolResponse()
