from pydantic import BaseModel, EmailStr


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
    email: EmailStr
    password: str


class ResetPasswordRequest(BaseModel):
    email: str


class ResetPasswordResponse(BaseModel):
    success: bool = True


class ResetPasswordConfirmRequest(BaseModel):
    code: str
    password: str


class ResetPasswordConfirmResponse(BaseModel):
    success: bool = True


class VerifyEmailResponse(BaseModel):
    success: bool = True


class ResendVerifyEmailResponse(BaseModel):
    success: bool = True
