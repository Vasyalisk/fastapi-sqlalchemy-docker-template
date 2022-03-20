from fastapi import Path

from uuid import UUID

from core.views import RetrieveAPIView
from users import models
from users import schemas


class UserDetailsView(RetrieveAPIView):
    model_class = models.User
    response_model = schemas.UserDetailResponse

    @staticmethod
    def get_request(user_uid: UUID = Path(...)) -> dict:
        return {"uid": user_uid}


class MyUserDetailsView(RetrieveAPIView):
    model_class = models.User
    response_model = schemas.UserDetailResponse
    is_authorized = True

    # noinspection PyMethodOverriding
    @staticmethod
    def get_request():
        return {}

    async def get_object(self):
        return self.user
