from fastapi import HTTPException

import functools
from typing import Optional

from core import crud
from core.serializers import DefaultSerializer
from security.deps import AuthUser


class APIView:
    http_methods = None
    dependencies = None
    response_model = None
    # response_model_extra = {
    #     "response_model_include": None,
    #     "response_model_exclude": None,
    #     "response_model_by_alias": True,
    #     "response_model_exclude_unset": False,
    #     "response_model_exclude_defaults": False,
    #     "response_model_exclude_none": False,
    # }
    response_model_extra = {}

    model_class = None
    serializer_class = None

    def __init__(self):
        self.kwargs = {}
        self.authorization: Optional[AuthUser] = None

    @classmethod
    def as_view(cls):
        func = cls.get_request_signature

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            instance = cls()
            instance.authorization = kwargs.pop("authorization", None)
            instance.args = args
            instance.kwargs = kwargs

            if instance.authorization:
                await instance.authorization.requires_access_token()

            result = await instance.on_request()
            return result

        return wrapper

    def raise_404(self, detail=None):
        raise HTTPException(status_code=404, detail=detail)

    def raise_400(self, detail=None):
        raise HTTPException(status_code=400, detail=detail)

    @staticmethod
    def get_request_signature(*args, **kwargs):
        pass

    async def on_request(self):
        raise NotImplemented()

    async def get_object(self):
        model = await crud.get_or_none(
            model_class=self.model_class,
            **self.kwargs
        )
        return model

    async def get_serializer(self, model):
        if self.serializer_class is None:
            self.serializer_class = DefaultSerializer

        serializer = await self.serializer_class.get_instance(
            model=model,
            **self.kwargs
        )
        return serializer


class RetrieveAPIView(APIView):
    http_methods = ["get"]

    @staticmethod
    def get_request_signature(id: int):
        pass

    async def on_request(self):
        model = await self.get_object()

        if model is None:
            self.raise_404()

        serializer = await self.get_serializer(model)
        response = await serializer.get()
        return response


class UpdateAPIView(APIView):
    http_methods = ["patch", "put"]

    @staticmethod
    def get_request_signature(id: int):
        pass

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

    @staticmethod
    def get_request_signature(id: int):
        pass

    async def on_request(self):
        model = await self.get_object()

        if model is None:
            self.raise_404()

        serializer = await self.get_serializer(None)
        response = await serializer.delete()
        return response
