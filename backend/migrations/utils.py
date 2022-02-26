import importlib
import os
from functools import wraps
from subprocess import Popen

from config import settings


def import_models():
    model_modules = []
    for name in settings.INSTALLED_APPS:
        module = _import_or_none(f"{name}.models")
        if module:
            model_modules.append(module)

    return model_modules


def _import_or_none(name, package=None):
    try:
        return importlib.import_module(name=name, package=package)
    except ImportError:
        return None


def with_alembic_workdir(func):
    alembic_workdir = settings.MIGRATIONS_DIR.split("/")
    alembic_workdir = "/".join(alembic_workdir[:-1])
    curr_dir = os.getcwd()

    @wraps(func)
    def wrapper(*args, **kwargs):
        os.chdir(alembic_workdir)
        result = func(*args, **kwargs)
        os.chdir(curr_dir)
        Popen(["chmod", "-R", "777", settings.MIGRATIONS_DIR])
        return result

    return wrapper
