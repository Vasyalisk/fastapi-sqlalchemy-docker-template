from config import settings
from users import crud as users_crud
from mail import utils


async def send_email(ctx, email_type: str, **kwargs):
    sender_map = {
        "reset_password": send_reset_password_email,
    }
    sender = sender_map.get(email_type)
    if sender is None:
        return

    await sender(ctx=ctx, **kwargs)


async def send_reset_password_email(ctx, user_id: int):
    user = await users_crud.get_one_by_id(user_id)

    if user is None:
        return

    code = ""
    text, html = utils.render_email("reset_password", code=code, project_name=settings.PROJECT_NAME)

    await utils.send_email(
        text=text,
        html=html,
        subject="Reset Password",
        to_emails=[user.email]
    )


functions = [
    send_email,
    send_reset_password_email,
]
