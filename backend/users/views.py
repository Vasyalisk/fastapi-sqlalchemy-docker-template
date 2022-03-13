from core.views import RetrieveAPIView, UpdateAPIView

from users import models
from users import schemas


class UserDetailsView(RetrieveAPIView):
    model_class = models.User
    response_model = schemas.UserDetailResponse


class MyUserDetailsView(RetrieveAPIView):
    model_class = models.User
    response_model = schemas.UserDetailResponse
    is_authorized = True

    # noinspection PyMethodOverriding
    @staticmethod
    async def get_request():
        return {}

    async def get_object(self):
        return self.user


class UserUpdateView(UpdateAPIView):
    http_methods = ["patch"]
    response_model = schemas.UserDetailResponse
    is_authorized = True

    # noinspection PyMethodOverriding
    @staticmethod
    def get_request(body_data: schemas.UserUpdateRequest):
        return {"body_data": body_data}

    async def get_object(self):
        return self.user
