from pydantic import BaseSettings
from typing import Optional

from config import settings as core_settings


class AdminSettings(BaseSettings):
    SECRET_KEY: str = core_settings.SECRET_KEY
    PROJECT_NAME: str = core_settings.PROJECT_NAME

    SQLALCHEMY_DATABASE_URI: str = core_settings.database_url_sync
    SQLALCHEMY_TRACK_MODIFICATIONS: Optional[bool] = False
    SQLALCHEMY_ECHO: Optional[bool] = False

    SECURITY_PASSWORD_SALT: str = core_settings.SECURITY_PASSWORD_SALT

    class Config:
        case_sensitive = True


settings = AdminSettings()
