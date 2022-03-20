from core.routers import ViewAPIRouter
from security import views
from security import schemas

router = ViewAPIRouter(prefix="/auth", tags=["auth"])

router.post("/login", response_model=schemas.TokensResponse)(views.login_view)
router.post("/register", response_model=schemas.TokensResponse)(views.register_view)
router.post("/refresh", response_model=schemas.TokensResponse)(views.refresh_tokens_view)
router.add_api_view_route("/reset_password", views.ResetPasswordView)
router.add_api_view_route("/reset_password/confirm", views.ResetPasswordConfirmView)
router.post("/email/verify", response_model=schemas.VerifyEmailResponse)(views.verify_email_view)
router.post("/email/resend_verification", response_model=schemas.ResendVerifyEmailResponse)(views.resend_verify_email)
