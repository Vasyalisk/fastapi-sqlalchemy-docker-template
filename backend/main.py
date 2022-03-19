from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from config import settings
from core import middleware
from core import utils as core_utils
from security import utils as security_utils
from admin.main import app as admin_app
from arq_queue import job_pool as task_pool

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
    app.mount("/admin", WSGIMiddleware(admin_app))
    security_utils.load_security_config()
    await task_pool.create_pool()


@app.on_event("shutdown")
async def on_shutdown():
    task_pool.close()
    await task_pool.wait_closed()
