from config import settings

import importlib

from fastapi import FastAPI


def add_routers(app: FastAPI):
    router_modules = (
        module
        for app_name in settings.INSTALLED_APPS
        if (module := _import_module_or_none(f"{app_name}.routers"))
    )
    [
        app.include_router(router, prefix="/api")
        for module in router_modules
        if (router := getattr(module, "router", None))
    ]


def _import_module_or_none(name, package=None):
    try:
        return importlib.import_module(name, package=package)
    except ImportError:
        return None
