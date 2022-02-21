from fastapi.requests import Request

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
