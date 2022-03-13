# Fastapi project template #

## Contents ##

1. Setting up docker-compose
2. Commands CLI
3. App structure
4. Class-based views
5. SQLAlchemy and alembic migration tool
6. Flask admin panel

## 1. Setting up docker-compose ##

- run either ```sh backend/scripts/setup_local_server.sh``` or ```sh backend/scripts/setup_prod_server.sh```
- fill in missing params in created .env file
- run ```docker-compose up``` (will raise validation errors in case some mandatory fields are missing)
- optionally run ```python manage.py createadmin <email> <password>``` inside docker to access admin panel
  at ```localhost/admin```

## 1. Commands CLI ##

- support for custom CLI commands in format ```python manage.py <command>```
- to create custom command put ```<command_name>.py``` file with function named ```command```
  into ```<app_name>/commands``` directory
- to access commands:
    - enter docker container ```docker-compose exec app bash```
    - list all commands ```python manage.py --help```
    - run ```python manage.py <command>```
- see official [Typer docs](https://typer.tiangolo.com) for defining custom commands

## 2. App structure ##

- all sub-apps are located in ```backend``` directory
- to create new sub-app:
    - run command ```python manage.py startapp <app_name>```
    - add app name to ```INSTALLED_APPS``` in ```config.py``` (see example in ```core.commands```)
- automatically detected features:
    - custom commands from ```<app_name>/commands``` are automatically added to
      ```python manage.py --help``` command list
    - SQLAlchemy model changes are automatically tracked from ```models.py```
    - instance of ```APIRouter``` or ```ViewAPIRouter``` from ```routers.py``` named as ```router``` is automatically
      mounted to the main app (see example in ```users.routers```)

## 3. Class-based views ##

- base view classes are defined in ```core.views```
- concrete implementation can be found in ```users.views```
- each view has following customizable methods/properties:
    - ```get_request``` defines input params for the request and returns evaluated objects
    - ```model_class``` SQLAlchemy model used in serialization
    - ```response_model``` Pydantic schema used for the response
    - ```get_response_model``` Returns response_model by default
    - ```serializer_class``` ```core.serializers.BaseSerializer``` subclass for serializing objects
    - ```is_authorized``` defines if API should have user authorization
    - ```authorize``` concrete implementation of user authorization using security.deps.AuthUser class
- views can be either mounted using ```core.routers.ViewAPIRouter``` (reduces boilerplate code)
  or ```fastapi.APIRouter```

## 4. SQLAlchemy and alembic migration tool ##

- all models are placed in ```<app_name>/models.py``` and are subclasses of ```database.models.BaseTable```
- to create automatic migrations run ```python manage.py makemigrations <optional_migration_name>```
- to upgrade database run ```python manage.py upgrade``` (applies all migrations) or ```python manage.py upgrade 1``` (
  applies single next migration)
- to downgrade run ```python manage.py downgrade``` (unapply most recent migration)
  or ```python manage.py downgrade -2``` (downgrade 2 most recent migrations)
- all generated migrations are located in ```migrations/versions```

## 5. Flask admin panel ##

- is served at ```localhost/admin```
- admin panel authorizes admin using cookies provided by Flask-Security
- to create admin view protected by admin authorization, use ```admin.views.mixins.AuthorizedAdminMixin``` (see example
  in ```admin.views.index.AuthorizedAdminIndexView```)
- to create admin user run ```python manage.py createadmin <email> <password>```