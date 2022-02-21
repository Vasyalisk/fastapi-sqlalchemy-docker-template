from fastapi import APIRouter

from security import views
from security import schemas

router = APIRouter(prefix="/auth")

router.add_api_route("/login", views.login_view, response_model=schemas.TokensResponse, methods=["post"])
router.add_api_route("/register", views.register_view, response_model=schemas.TokensResponse, methods=["post"])
