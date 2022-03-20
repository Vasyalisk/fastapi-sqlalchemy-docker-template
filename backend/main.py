from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from config import settings
from core.middleware import add_cors_middleware
from core.utils import add_routers
from security import utils as security_utils
from admin.main import app as admin_app
from arq_queue import job_pool
from redis_db import redis_client

app = FastAPI(
    title=settings.PROJECT_NAME + " API",
    description="FastAPI based backend app",
    version="1.0",
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)


@app.on_event("startup")
async def on_startup():
    add_cors_middleware(app)
    add_routers(app)
    app.mount("/admin", WSGIMiddleware(admin_app))
    security_utils.load_security_config()
    await job_pool.create_pool()
    await redis_client.create_pool()


@app.on_event("shutdown")
async def on_shutdown():
    job_pool.close()
    await job_pool.wait_closed()
    redis_client.close()
    await redis_client.wait_closed()
