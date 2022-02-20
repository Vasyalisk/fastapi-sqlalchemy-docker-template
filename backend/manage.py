from config import settings

import importlib
import pkgutil

import typer


def get_typer_app() -> typer.Typer:
    """
    Creates typer app and registers all cli commands from sub-apps
    :return:
    """
    cli_app = typer.Typer()
    connect_commands(cli_app)
    cli_app.callback()(lambda: None)
    return cli_app


def connect_commands(cli_app: typer.Typer):
    """
    Connect all commands from registered apps

    Commands are functions named 'command' placed in registered_app.commands sub-folder
    Command name is the same as module name. E.g. mail.commands.send_email will create command send_email
    :param cli_app:
    :return:
    """
    for app_name in settings.INSTALLED_APPS:
        rel_path = f"{app_name}/commands"
        rel_package = f"{app_name}.commands"
        [
            connect_command(cli_app, rel_package, module_info)
            for module_info in pkgutil.iter_modules([rel_path])
        ]


def connect_command(cli_app: typer.Typer, package_name, module_info: pkgutil.ModuleInfo):
    module_info: pkgutil.ModuleInfo
    if module_info.ispkg:
        return

    module = importlib.import_module(name=f"{package_name}.{module_info.name}")
    command = getattr(module, "command", None)

    if command is None:
        return

    cli_app.command(name=module_info.name)(command)


app = get_typer_app()

if __name__ == "__main__":
    app()
