from fastapi import APIRouter

from config import settings
from arq_queue import views

router = APIRouter(prefix="/arq", tags=["arq"])

if settings.DEBUG:
    router.add_api_route("/health_check", views.health_check_api, methods=["GET"])
