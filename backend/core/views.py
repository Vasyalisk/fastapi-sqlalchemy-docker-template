from fastapi import Depends, HTTPException, Path

import re

from security.utils import get_authorization
from security.deps import AuthUser

from core.serializers import DefaultSerializer
from core import crud

_camel_to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def _camel_to_snake(s):
    return _camel_to_snake_pattern.sub('_', s).lower()


class APIView:
    http_methods = None
    response_model = None
    is_authorized = False
    model_class = None
    serializer_class = None
    dependencies = []

    # Default values
    # response_model_extra = {
    #     "response_model_include": None,
    #     "response_model_exclude": None,
    #     "response_model_by_alias": True,
    #     "response_model_exclude_unset": False,
    #     "response_model_exclude_defaults": False,
    #     "response_model_exclude_none": False,
    # }
    response_model_extra = {}

    def __init__(self):
        self.request_data = {}
        self.user = None

    @staticmethod
    async def get_request() -> dict:
        return {}

    @classmethod
    def get_response_model(cls):
        return cls.response_model

    @staticmethod
    async def authorize(authorization: AuthUser = Depends(get_authorization)):
        await authorization.requires_access_token()
        return authorization.get_user()

    @classmethod
    def as_view(cls):
        if cls.is_authorized:
            view = cls._as_authorized_view()
        else:
            view = cls._as_anonymous_view()

        view.__doc__ = cls.__doc__
        view.__name__ = _camel_to_snake(cls.__name__)
        return view

    @classmethod
    def _as_authorized_view(cls):
        async def wrapper(
                user: AuthUser = Depends(cls.authorize),
                request_data: dict = Depends(cls.get_request)
        ):
            view = cls()
            view.request_data = request_data
            view.user = user
            return await view.on_request()

        return wrapper

    @classmethod
    def _as_anonymous_view(cls):
        async def wrapper(
                request_data: dict = Depends(cls.get_request)
        ):
            view = cls()
            view.request_data = request_data
            return await view.on_request()

        return wrapper

    async def on_request(self):
        raise NotImplemented()

    def raise_404(self, detail=None):
        raise HTTPException(status_code=404, detail=detail)

    def raise_400(self, detail=None):
        raise HTTPException(status_code=400, detail=detail)

    async def get_object(self):
        model = await crud.get_or_none(
            model_class=self.model_class,
            **self.request_data
        )
        return model

    async def get_serializer(self, model):
        if self.serializer_class is None:
            self.serializer_class = DefaultSerializer

        serializer = await self.serializer_class.get_instance(
            model=model,
            **self.request_data
        )
        return serializer


class RetrieveAPIView(APIView):
    http_methods = ["get"]

    @staticmethod
    def get_request(model_id: int = Path(...)) -> dict:
        return {"id": model_id}

    async def on_request(self):
        model = await self.get_object()

        if model is None:
            self.raise_404()

        serializer = await self.get_serializer(model)
        response = await serializer.get()
        return response


class UpdateAPIView(APIView):
    http_methods = ["patch", "put"]
    lookup_kwarg = "id"

    @staticmethod
    def get_request(model_id: int = Path(...)):
        return {"id": model_id}

    async def get_object(self):
        model = await crud.get_or_none(
            model_class=self.model_class,
            **{self.lookup_kwarg: self.request_data.get(self.lookup_kwarg)}
        )
        return model

    async def on_request(self):
        model = await self.get_object()

        if model is None:
            self.raise_404()

        serializer = await self.get_serializer(model)
        response = await serializer.update()
        return response


class CreateAPIVIew(APIView):
    http_methods = ["post"]

    async def on_request(self):
        serializer = await self.get_serializer(None)
        response = await serializer.create()
        return response


class DestroyAPIView(APIView):
    http_methods = ["delete"]
    lookup_kwarg = "id"

    @staticmethod
    def get_request(model_id: int = Path(...)):
        return {"id": model_id}

    async def get_object(self):
        model = await crud.get_or_none(
            model_class=self.model_class,
            **{self.lookup_kwarg: self.request_data.get(self.lookup_kwarg)}
        )
        return model

    async def on_request(self):
        model = await self.get_object()

        if model is None:
            self.raise_404()

        serializer = await self.get_serializer(None)
        response = await serializer.delete()
        return response
