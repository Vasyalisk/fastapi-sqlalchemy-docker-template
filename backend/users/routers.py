from fastapi import APIRouter

from users import views
from users import schemas

router = APIRouter(prefix='/users')

router.add_api_route("/{id}/details/", views.APIView.as_view(), response_model=schemas.UserDetailResponse)
