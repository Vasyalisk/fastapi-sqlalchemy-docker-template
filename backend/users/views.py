from fastapi import HTTPException

from functools import wraps

from users import crud


class APIView:
    lookup_url_kwarg = "id"
    lookup_field = "id"
    http_methods = ["get"]

    @classmethod
    def as_view(cls):
        func = cls.get_dependencies

        @wraps(func)
        async def wrapper(*args, **kwargs):
            instance = cls()
            deps = func(*args, **kwargs)
            result = await instance.on_request(**deps)
            return result

        return wrapper

    def raise_404(self, detail=None):
        raise HTTPException(status_code=404, detail=detail)

    @staticmethod
    def get_dependencies(
            id: int
    ):
        return {
            "id": id
        }

    async def on_request(self, **deps):
        payload = {
            self.lookup_field: deps.get(self.lookup_url_kwarg)
        }
        model = await crud.get_user_or_none(**payload)

        if model is None:
            self.raise_404()

        return model
