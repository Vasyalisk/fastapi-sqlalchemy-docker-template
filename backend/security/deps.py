from fastapi import Request, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from werkzeug.security import check_password_hash

from typing import Optional

from users import models
from security import schemas
from security import crud

api_key_header = Security(APIKeyHeader(name="Authorization", auto_error=False))


class AuthUser:
    """
    Class for authenticating user. Authentication is possible by bearer token or login.
    Use as dependency injection:
        authorize: AuthUser = Depends()
        await authorize.requires_access_token()
    """

    def __init__(self, request: Request):
        """
        :param request: Incoming request to current API endpoint
        """
        self.request = request
        self.body = None
        self.user: Optional[models.User] = None

    def _raise_unauthorized(self, detail=None):
        self.user = None
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    def _raise_400(self, detail=None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    async def get_body(self) -> dict:
        if self.body is None:
            try:
                self.body = await self.request.json()
            except Exception:
                self.body = dict()
        return self.body

    def get_user(self):
        if self.user is None:
            self._raise_unauthorized()
        return self.user

    async def requires_access_token(self):
        """
        Authorize user using jwt Bearer token from Authorization header
        :raise: token-related HTTPExceptions from AuthJWT
        :raise: HTTPException 401 if no user with corresponding token exists
        :return:
        """
        jwt_authorize = AuthJWT(req=self.request)
        jwt_authorize.jwt_required()
        user_id = jwt_authorize.get_jwt_subject()
        user = await crud.get_user_by_id(user_id)

        if user is None:
            self._raise_unauthorized()

        self.user = user

    async def requires_login(self, validated_data: schemas.LoginRequest):
        """
        Authorize exiting user if password corresponds to username
        :param validated_data:
        :return:
        """

        user = await crud.get_user_by_username(validated_data.username)
        if user is None:
            self._raise_unauthorized()

        is_valid_password = check_password_hash(user.password, password=validated_data.password)

        if not is_valid_password:
            self._raise_unauthorized()

        self.user = user

    async def requires_refresh_token(self):
        jwt_authorize = AuthJWT(req=self.request)
        jwt_authorize.jwt_refresh_token_required()
        user_id = jwt_authorize.get_jwt_subject()

        user = await crud.get_user_by_id(user_id)

        if user is None:
            self._raise_unauthorized()

        self.user = user

    def create_tokens(self) -> schemas.TokensResponse:
        """
        Requires self.user being not None
        :raise: HTTPException 401 if no user
        :return:
        """
        if self.user is None:
            self._raise_unauthorized()
        jwt_authorize = AuthJWT(self.request)
        access_token = jwt_authorize.create_access_token(subject=self.user.id)
        refresh_token = jwt_authorize.create_refresh_token(subject=self.user.id)
        return schemas.TokensResponse(access_token=access_token, refresh_token=refresh_token)

    def get_raw_jwt(self, encoded_token=None) -> dict:
        """
        Returns dict of info encoded in token
        :param encoded_token:
        :return:
        """
        jwt_authorize = AuthJWT(self.request)
        return jwt_authorize.get_raw_jwt(encoded_token=encoded_token)
