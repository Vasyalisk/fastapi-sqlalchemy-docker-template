from pydantic import BaseModel

from config import settings as base_settings


class SecuritySettings(BaseModel):
    authjwt_token_location = ('headers', 'cookies')
    authjwt_access_cookie_key = "token"
    authjwt_cookie_csrf_protect = False

    authjwt_secret_key = base_settings.SECRET_KEY
    authjwt_access_token_expires = base_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    authjwt_refresh_token_expires = base_settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60

    RESET_TOKEN_LENGTH: int = 5
    RESET_TOKEN_EXPIRE_MIN: float = 5.0


settings = SecuritySettings()
