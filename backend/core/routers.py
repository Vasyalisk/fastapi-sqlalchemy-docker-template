from fastapi import APIRouter
from fastapi.datastructures import Default
from fastapi.responses import JSONResponse


class ViewAPIRouter(APIRouter):
    def add_api_view_route(
            self,
            path: str,
            view,
            *,
            response_model=None,
            status_code=None,
            tags=None,
            dependencies=None,
            summary=None,
            description=None,
            response_description: str = "Successful Response",
            responses=None,
            deprecated=None,
            methods=None,
            operation_id=None,
            response_model_include=None,
            response_model_exclude=None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class=Default(JSONResponse),
            name=None,
            route_class_override=None,
            callbacks=None,
            openapi_extra=None,
    ) -> None:
        endpoint = view.as_view()
        response_model = view.get_response_model() or response_model
        dependencies = view.dependencies or dependencies
        methods = view.http_methods or methods

        response_model_include = view.response_model_extra.get("response_model_include", response_model_include)
        response_model_exclude = view.response_model_extra.get("response_model_exclude", response_model_exclude)
        response_model_by_alias = view.response_model_extra.get("response_model_by_alias", response_model_by_alias)
        response_model_exclude_unset = view.response_model_extra.get(
            "response_model_exclude_unset",
            response_model_exclude_unset
        )
        response_model_exclude_defaults = view.response_model_extra.get(
            "response_model_exclude_defaults",
            response_model_exclude_defaults
        )
        response_model_exclude_none = view.response_model_extra.get(
            "response_model_exclude_none",
            response_model_exclude_none
        )

        return self.add_api_route(
            path=path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            route_class_override=route_class_override,
            callbacks=callbacks,
            openapi_extra=openapi_extra
        )
