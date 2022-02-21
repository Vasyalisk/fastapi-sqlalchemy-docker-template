from pydantic import BaseModel


class TokensResponse(BaseModel):
    """
    Refresh and access token pair
    """

    access_token: str
    refresh_token: str


class LoginRequest(BaseModel):
    """
    Payload to confirm user login
    """
    username: str
    password: str


class RegisterRequest(BaseModel):
    """
    Payload to register user
    """
    username: str
    password: str
