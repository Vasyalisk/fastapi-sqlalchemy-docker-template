from importlib import import_module

from config import settings


def detect_jobs():
    task_modules = (
        module
        for app in settings.INSTALLED_APPS
        if (module := _import_or_none(f"{app}.jobs"))
    )
    task_routes = (
        (
            getattr(module, "functions", []),
            getattr(module, "cron_jobs", [])
        )
        for module in task_modules
    )

    tasks = []
    cron_jobs = []
    [
        (
            tasks.extend(one[0]),
            cron_jobs.extend(one[1])
        )
        for one in task_routes
    ]
    return tasks, cron_jobs


def _import_or_none(name, package=None):
    try:
        return import_module(name=name, package=package)
    except ImportError:
        return None
