from fastapi import APIRouter

from mail import views
from mail import schemas

router = APIRouter(prefix='/mail', tags=["mail"])

router.add_api_route(
    "/send_test_email",
    views.send_test_email_api,
    methods=["POST"],
    response_model=schemas.SendTestEmailResponse
)
