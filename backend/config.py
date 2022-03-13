from typing import (
    List,
    Optional,
    Union
)

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    validator
)


class Settings(BaseSettings):
    # --- Base section ---
    PROJECT_NAME: str
    SECRET_KEY: str

    DEBUG: Optional[bool] = False
    ECHO_SQL: Optional[bool] = False
    TESTING: Optional[bool] = False

    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:3002",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # noinspection PyPep8Naming
    @property
    def INSTALLED_APPS(self):
        return [
            "core",
            "database",
            "users",
            "security",
            "migrations",
            "admin",
        ]

    # --- Redis section ---
    REDIS_SERVER: str
    REDIS_PASSWORD: str
    REDIS_APP_DB: Optional[int] = 0
    REDIS_CELERY_DB: Optional[int] = 1

    HASH_ENCODING: Optional[str] = "utf8"

    # --- DB section ---
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'

    @property
    def database_url_sync(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'

    # --- Authentication section ---
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: Optional[int] = 60 * 24 * 7

    # --- Migrations section ---
    MIGRATIONS_DIR: str = "/backend/migrations/versions"

    # --- Admin section ---
    SECURITY_PASSWORD_SALT: str

    class Config:
        case_sensitive = True


settings = Settings()
