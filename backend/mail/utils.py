import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

from database.utils import with_session, AsyncSession
from mail.config import settings
from mail.config import email_environment
from mail import crud as mail_crud


def render_email(template_name, **kwargs) -> tuple[str, str]:
    if template_name not in settings.registered_templates:
        raise ValueError(f"{template_name} template is not registered in mail.config.settings!") from None

    text_template = email_environment.get_template(f"text/{template_name}.txt")
    html_template = email_environment.get_template(f"html/{template_name}.html")

    return text_template.render(**kwargs), html_template.render(**kwargs)


@with_session
async def send_email(
        text: str,
        html: str,
        subject: str,
        to_emails: list[str],
        session: AsyncSession = None
):
    model = await mail_crud.create(
        from_email=settings.FROM_EMAIL,
        to_emails=to_emails,
        content_text=text,
        content_html=html,
        subject=subject
    )

    email = MIMEMultipart()
    email["Subject"] = subject
    email.attach(MIMEText(text, "plain", "utf-8"))
    email.attach(MIMEText(html, "html", "utf-8"))

    try:
        errors, response = await aiosmtplib.send(
            email,
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            sender=settings.FROM_EMAIL,
            recipients=to_emails,
            username=settings.EMAIL_USERNAME,
            password=settings.EMAIL_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        )
    except Exception:
        return False

    if errors:
        return False

    model.sent_time = datetime.now()
    session.add(model)
    await session.commit()
    return True
