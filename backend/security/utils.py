from fastapi.requests import Request
from werkzeug.security import check_password_hash as check_password_hash
from werkzeug.security import generate_password_hash as generate_password_hash

import secrets

from security.config import settings
from security import deps


def get_authorization(
        request: Request,
        auth_header: str = deps.api_key_header
) -> deps.AuthUser:
    yield deps.AuthUser(request=request)


def get_headerless_authorization(
        request: Request
) -> deps.AuthUser:
    yield deps.AuthUser(request=request)


def load_security_config():
    from fastapi_jwt_auth import AuthJWT
    from security.config import SecuritySettings
    
    # noinspection PyTypeChecker
    AuthJWT.load_config(SecuritySettings)


def generate_reset_code() -> str:
    code = secrets.randbelow(10 ** settings.RESET_TOKEN_LENGTH)
    code = f"{code:0{settings.RESET_TOKEN_LENGTH}}"
    return code
