from pydantic import BaseModel

from config import settings as app_settings


class RedisConfig(BaseModel):
    REDIS_HOST: str = app_settings.REDIS_HOST
    REDIS_PORT: int = app_settings.REDIS_PORT
    REDIS_PASSWORD: str = app_settings.REDIS_PASSWORD
    REDIS_APP_DB: int = app_settings.REDIS_APP_DB

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/"


settings = RedisConfig()
