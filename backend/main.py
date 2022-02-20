from config import settings
from core import middleware
from core import utils

from fastapi import FastAPI

app = FastAPI(
    title=settings.PROJECT_NAME + " API",
    description="FastAPI based backend app",
    version="1.0",
    redoc_url=None
)


@app.on_event("startup")
async def on_startup():
    middleware.add_cors_middleware(app)
    utils.add_routers(app)


@app.on_event("shutdown")
async def on_shutdown():
    pass
