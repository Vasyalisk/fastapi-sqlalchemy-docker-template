from config import settings

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def add_cors_middleware(app: FastAPI):
    if not settings.BACKEND_CORS_ORIGINS:
        return

    allow_cors = "*" if settings.DEBUG else [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_cors,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
