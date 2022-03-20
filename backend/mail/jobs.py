from config import settings
from users import crud as users_crud
from mail import utils
from redis_db import redis_client


async def send_email(ctx, template_name: str, **kwargs):
    sender_map = {
        "reset_password": send_reset_password_email,
        "verify_email": send_verify_email,
    }
    sender = sender_map.get(template_name)
    if sender is None:
        return

    await sender(ctx=ctx, **kwargs)


async def send_reset_password_email(ctx, user_id: int, code: str):
    user = await users_crud.get_one_by_id(user_id)

    if user is None:
        return

    text, html = utils.render_email(
        "reset_password",
        code=code,
        project_name=settings.PROJECT_NAME
    )

    await utils.send_email(
        text=text,
        html=html,
        subject="Reset Password",
        to_emails=[user.email]
    )


async def send_verify_email(ctx, user_id: int):
    user = await users_crud.get_one_by_id(user_id)

    if user is None:
        return

    link = f"{settings.FE_DOMAIN}/verify_email"
    text, html = utils.render_email(
        "verify_email",
        link=link,
        project_name=settings.PROJECT_NAME
    )
    await utils.send_email(
        text=text,
        html=html,
        subject="Verify Email",
        to_emails=[user.email]
    )


functions = [
    send_email,
    send_reset_password_email,
    send_verify_email,
]
