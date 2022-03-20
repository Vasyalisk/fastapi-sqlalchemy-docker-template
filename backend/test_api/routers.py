from core.routers import ViewAPIRouter

from config import settings
from test_api import views
from test_api import schemas

router = ViewAPIRouter(prefix='/test', tags=["test"])

if settings.DEBUG:
    router.post("/send_test_email", response_model=schemas.SendTestEmailResponse)(views.send_test_email_view)
    router.get("/health_check", response_model=schemas.BoolResponse)(views.health_check_view)
