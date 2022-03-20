from fastapi import Depends

from core import ErrorMessage
from core.views import CreateAPIVIew
from security.config import settings
from database import utils as db_utils
from redis_db import redis_client
from arq_queue import job_pool

from security import schemas
from security import deps
from security import utils
from security import crud


async def login_view(
        post_data: schemas.LoginRequest,
        authorization: deps.AuthUser = Depends(utils.get_headerless_authorization)
):
    await authorization.requires_login(post_data)
    return authorization.create_tokens()


async def register_view(
        post_data: schemas.RegisterRequest,
        authorization: deps.AuthUser = Depends(utils.get_headerless_authorization)
):
    post_data.password = utils.generate_password_hash(post_data.password)
    user = await crud.register_user(**post_data.dict())
    await job_pool.enqueue_job(
        "send_email",
        "verify_email",
        user_id=user.id,
    )

    authorization.user = user
    return authorization.create_tokens()


async def refresh_tokens_view(
        authorization: deps.AuthUser = Depends(utils.get_authorization)
):
    await authorization.requires_refresh_token()
    return authorization.create_tokens()


class ResetPasswordView(CreateAPIVIew):
    response_model = schemas.ResetPasswordResponse

    # noinspection PyMethodOverriding
    @staticmethod
    def get_request(post_data: schemas.ResetPasswordRequest) -> dict:
        return {"email": post_data.email}

    async def on_request(self):
        self.user = await crud.get_user(email=self.request_data["email"])

        if self.user is not None:
            await self.set_code()
            await self.send_email()

        return schemas.ResetPasswordResponse()

    async def set_code(self):
        code = utils.generate_reset_code()
        await redis_client.set(
            f"reset_code:{code}",
            self.user.id,
            expire=int(settings.RESET_TOKEN_EXPIRE_MIN * 60)
        )
        self.request_data["code"] = code

    async def send_email(self):
        await job_pool.enqueue_job(
            "send_email",
            "reset_password",
            user_id=self.user.id,
            code=self.request_data["code"]
        )


class ResetPasswordConfirmView(CreateAPIVIew):
    response_model = schemas.ResetPasswordConfirmResponse

    # noinspection PyMethodOverriding
    @staticmethod
    def get_request(post_data: schemas.ResetPasswordConfirmRequest) -> dict:
        return {"code": post_data.code, "password": post_data.password}

    async def on_request(self):
        await self.get_user()
        await self.set_new_password()
        await self.delete_code()
        return {}

    async def get_user(self):
        code = self.request_data["code"]
        user_id = await redis_client.get(f"reset_code:{code}", encoding=redis_client.ENCODING)

        if user_id is None:
            self.raise_400(ErrorMessage.INVALID_PASSWORD_RESET_CODE)

        user = await crud.get_user(id=int(user_id))

        if user is None:
            self.raise_400(ErrorMessage.INVALID_PASSWORD_RESET_CODE)

        self.user = user

    @db_utils.with_session()
    async def set_new_password(self, session: db_utils.AsyncSession = None):
        password = self.request_data["password"]
        self.user.password = utils.generate_password_hash(password)
        session.add(self.user)
        await session.commit()

    async def delete_code(self):
        code = self.request_data["code"]
        await redis_client.delete(f"reset_code:{code}")


async def verify_email_view(
        authorization: deps.AuthUser = Depends(utils.get_authorization),
        session: db_utils.AsyncSession = Depends(db_utils.get_async_session)
):
    await authorization.requires_access_token()
    user = authorization.get_user()

    user.is_email_verified = True
    session.add(user)
    await session.commit()

    return schemas.VerifyEmailResponse()


async def resend_verify_email(
        authorization: deps.AuthUser = Depends(utils.get_authorization)
):
    await authorization.requires_access_token()
    user = authorization.get_user()

    await job_pool.enqueue_job(
        "send_email",
        "verify_email",
        user_id=user.id
    )

    return schemas.ResendVerifyEmailResponse()
