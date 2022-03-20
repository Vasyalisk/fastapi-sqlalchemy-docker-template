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
