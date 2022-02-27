from fastapi import HTTPException, status

from pydantic import BaseModel
from typing import Iterable, Optional

from core import crud


def perform_if_exists(func):
    """
    Decorator for BaseFieldSerializer for skipping validation/update on fields which are not present in update_data
    Example usage:
        @classmethod
        @perform_if_exists
        async def validate(cls, user: models.User, *, update_data: dict):
    :param func:
    :return:
    """

    async def wrapper(cls, *args, **kwargs):
        validated_data = kwargs.get("validated_data")

        if validated_data is None:
            return

        if cls.FIELD not in validated_data:
            return

        return await func(cls, *args, **kwargs)

    return wrapper


class BaseFieldSerializer:
    """
    Base sub-component class for BaseSerializer
    Subclass it and put relative subclass in
        BaseSerializer.FIELD_VALIDATORS,
        BaseSerializer.FIELD_PREPARATORS,
        BaseSerializer.FIELD_UPDATERS,
        BaseSerializer.FIELD_FINISHERS
    as needed
    """
    FIELD = None

    @classmethod
    def raise_404(cls, detail=None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    @classmethod
    def raise_400(cls, detail=None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    @classmethod
    async def validate(
            cls, *,
            model=None,
            validated_data: dict
    ):
        """
        Additionally validate input data without updating anything, used to raise various HTTP exceptions
        :param model:
        :param validated_data:
        :return:
        """
        raise NotImplementedError()

    @classmethod
    async def prepare(
            cls, *,
            model=None,
            validated_data: dict,
    ):
        """
        Prepare input data/model for updates. E.g. create necessary properties in advance.
        :param model:
        :param validated_data:
        :return:
        """
        raise NotImplementedError()

    @classmethod
    async def finish(
            cls, *,
            model=None,
            validated_data: dict,
    ):
        """
        Perform other non-updating actions after update is complete. E.g. send email confirmation
        :param model:
        :param validated_data:
        :return:
        """
        raise NotImplementedError()


class BaseSerializer:
    """
    Serializer for updating, creating or getting model/response
    Use BaseSerializer.get_instance to create new serializer asynchronously
    Then run
    await serializer.validate_fields() - validates data and throws HTTP exceptions
    await serializer.prepare_fields() - prepares model and data for updates/creation
    await serializer.update_fields() - updates model and related models
    await serializer.finish_fields() - performs post-update/create actions
    UPDATE_FIELDS - list of simple DB fields which are updated directly by ORM
    CREATE_FIELDS - list of simple DB fields which are passed to model creation
    FIELD_VALIDATORS - instances of BaseFieldSerializer run in the validate_fields()
    FIELD_PREPARERS - instances of BaseFieldSerializer run in the prepare_fields()
    FIELD_UPDATERS - instances of BaseFieldSerializer run in update_fields()
    FIELD_FINISHERS - instances of BaseFieldSerializer run in finish_updates()
    MODEL_TYPE - class of SqlAlchemy model
    SCHEMA_TYPE - pydantic schema used to pass data in
    """
    update_fields_names = []
    create_fields_names = []
    find_field_names = []

    field_validators: Iterable["BaseFieldSerializer"] = []
    field_preparers: Iterable["BaseFieldSerializer"] = []
    field_updaters: Iterable["BaseFieldSerializer"] = []
    field_finishers: Iterable["BaseFieldSerializer"] = []

    model_class = None
    schema_class = BaseModel

    def __init__(self):
        self.validated_data: dict = dict()
        self.model: Optional[BaseSerializer.model_class] = None

    @classmethod
    async def get_instance(
            cls,
            model: Optional[model_class],
            **deps,
    ) -> "BaseSerializer":
        instance = cls()
        instance.validated_data = cls.get_validated_data(**deps)
        instance.model = model
        return instance

    @classmethod
    def get_validated_data(cls, **deps):
        validated_data = {}

        for value in deps.values():
            if not issubclass(type(value), BaseModel):
                continue
            validated_data = value.dict(exclude_unset=True)
            break

        return validated_data

    async def validate_fields(self) -> dict:
        [
            await validator.validate(model=self.model, validated_data=self.validated_data)
            for validator in self.field_validators
        ]
        return self.validated_data

    async def prepare_fields(self) -> dict:
        [
            await preparer.prepare(model=self.model, validated_data=self.validated_data)
            for preparer in self.field_preparers
        ]
        return self.validated_data

    async def update_model(self) -> dict:
        kwargs = {key: self.validated_data[key] for key in self.update_fields_names if key in self.validated_data}
        self.model = await crud.update(self.model, **kwargs)

        return self.validated_data

    async def create_model(self) -> model_class:
        kwargs = {key: self.validated_data[key] for key in self.create_fields_names if key in self.validated_data}
        self.model = await crud.create(self.model_class, **kwargs)
        return self.model

    async def get_model(self) -> model_class:
        kwargs = {key: self.validated_data[key] for key in self.find_field_names if key in self.validated_data}
        self.model = await crud.get_or_none(self.model_class, **kwargs)
        return self.model

    async def delete_model(self):
        self.model = None
        return None

    async def finish_fields(self) -> dict:
        [
            await finisher.finish(model=self.model, validated_data=self.validated_data)
            for finisher in self.field_finishers
        ]
        return self.validated_data

    async def create(self):
        """
        Shortcut for using all creation steps
        :return:
        """
        await self.validate_fields()
        await self.prepare_fields()
        await self.create_model()
        await self.finish_fields()
        return self.model

    async def update(self):
        """
        Shortcut for using all update steps
        :return:
        """
        await self.validate_fields()
        await self.prepare_fields()
        await self.update_model()
        await self.finish_fields()
        return self.model

    async def get(self):
        """
        Shortcut for using all get steps
        :return:
        """
        await self.validate_fields()
        await self.prepare_fields()
        await self.get_model()
        await self.finish_fields()
        return self.model

    async def delete(self):
        await self.validate_fields()
        await self.prepare_fields()
        await self.delete_model()
        await self.finish_fields()
        return {}


class DefaultSerializer(BaseSerializer):
    @classmethod
    async def get_instance(
            cls,
            model,
            **deps,
    ) -> "DefaultSerializer":
        instance = await super().get_instance(model, **deps)
        field_names = list(instance.validated_data.keys())
        instance.model_class = model.__class__
        instance.update_fields_names = field_names
        instance.create_fields_names = field_names
        instance.find_field_names = field_names
        return instance
