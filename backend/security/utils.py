from fastapi.requests import Request
from werkzeug.security import check_password_hash as check_password_hash
from werkzeug.security import generate_password_hash as generate_password_hash

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
    from security.config import JWTSettings
    AuthJWT.load_config(JWTSettings)
