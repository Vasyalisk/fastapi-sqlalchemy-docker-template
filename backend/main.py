from config import settings
from core import middleware
from core import utils as core_utils
from security import utils as security_utils

from fastapi import FastAPI

app = FastAPI(
    title=settings.PROJECT_NAME + " API",
    description="FastAPI based backend app",
    version="1.0",
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)


@app.on_event("startup")
async def on_startup():
    middleware.add_cors_middleware(app)
    core_utils.add_routers(app)
    security_utils.load_security_config()


@app.on_event("shutdown")
async def on_shutdown():
    pass
