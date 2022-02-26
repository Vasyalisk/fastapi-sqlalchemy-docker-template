from pydantic import BaseModel

from config import settings


class JWTSettings(BaseModel):
    authjwt_token_location = ('headers', 'cookies')
    authjwt_access_cookie_key = "token"
    authjwt_cookie_csrf_protect = False

    authjwt_secret_key = settings.SECRET_KEY
    authjwt_access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    authjwt_refresh_token_expires = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
