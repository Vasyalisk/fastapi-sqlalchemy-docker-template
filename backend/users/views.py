from core.views import RetrieveAPIView, UpdateAPIView
from fastapi import Depends

from users import models
from users import schemas
import security.utils


class UserDetailsView(RetrieveAPIView):
    model_class = models.User
    response_model = schemas.UserDetailResponse


class MyUserDetailsView(RetrieveAPIView):
    model_class = models.User
    requires_authorization = True
    response_model = schemas.UserDetailResponse

    @staticmethod
    def get_request_signature(
            authorization=Depends(security.utils.get_authorization)
    ):
        pass

    async def get_object(self):
        return self.authorization.get_user()


class UserUpdateView(UpdateAPIView):
    http_methods = ["patch"]
    requires_authorization = True
    response_model = schemas.UserDetailResponse

    @staticmethod
    def get_request_signature(
            validated_data: schemas.UserUpdateRequest,
            authorization=Depends(security.utils.get_authorization),
    ):
        pass

    async def get_object(self):
        return self.authorization.get_user()
