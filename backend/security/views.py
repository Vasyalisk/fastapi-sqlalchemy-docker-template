from fastapi import Depends

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

    authorization.user = user
    return authorization.create_tokens()


async def refresh_tokens_view(
        authorization: deps.AuthUser = Depends(utils.get_authorization)
):
    await authorization.requires_refresh_token()
    return authorization.create_tokens()
