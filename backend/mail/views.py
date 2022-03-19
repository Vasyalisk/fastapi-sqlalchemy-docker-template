from mail import schemas
from mail import utils


async def send_test_email_api(
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
    return {"is_sent": is_sent}
