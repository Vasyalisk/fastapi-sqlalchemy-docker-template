from fastapi import APIRouter

from config import settings
from mail import views
from mail import schemas

router = APIRouter(prefix='/mail', tags=["mail"])

if settings.DEBUG:
    router.add_api_route(
        "/send_test_email",
        views.send_test_email_api,
        methods=["POST"],
        response_model=schemas.SendTestEmailResponse
    )
