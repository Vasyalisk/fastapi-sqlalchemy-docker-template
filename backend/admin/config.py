from pydantic import BaseSettings
from typing import Optional

from config import settings as core_settings


class AdminSettings(BaseSettings):
    SECRET_KEY: Optional[str] = core_settings.SECRET_KEY
    PROJECT_NAME: Optional[str] = core_settings.PROJECT_NAME

    SQLALCHEMY_DATABASE_URI: Optional[str] = core_settings.database_url_sync
    SQLALCHEMY_TRACK_MODIFICATIONS: Optional[bool] = False
    SQLALCHEMY_ECHO: Optional[bool] = False

    SECURITY_PASSWORD_SALT: str

    class Config:
        case_sensitive = True


settings = AdminSettings()
