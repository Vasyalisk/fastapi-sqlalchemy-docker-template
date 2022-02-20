import typing
import re

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: typing.Dict = {}


def camel_to_snake(s: str) -> str:
    """
    CamelCase to snake_case converter:
        s = "theMixedCase"
        s = camel_to_snake(s) -> "the_mixed_case"
    :param s:
    :return:
    """

    words = re.split("(?=[A-Z])", s)
    words = (one.lower() for one in words if one)  # generator
    return "_".join(words)


@as_declarative(class_registry=class_registry)
class BaseTable:
    id: typing.Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically
        """
        name = camel_to_snake(cls.__name__)

        # user is a reserved keyword in SQL and is not recommended for table name
        if name == "user":
            name = "app_user"

        return name
