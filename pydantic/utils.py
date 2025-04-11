from collections.abc import Callable, Iterator
from datetime import datetime
from typing import Any

from bson import ObjectId
from pydantic_core import CoreSchema, core_schema

from pydantic import BaseModel, ConfigDict, GetJsonSchemaHandler
from pydantic._internal._core_utils import CoreSchemaOrField, is_core_schema
from pydantic.json_schema import GenerateJsonSchema


def delete_empty_default(schema):
    for key in list(schema):
        if key == "default" and schema["default"] is None:
            schema.pop("default")
            continue
        if isinstance(schema[key], dict):
            delete_empty_default(schema[key])

class GenerateJsonSchemaWithoutDefaultTitles(GenerateJsonSchema):
    def field_title_should_be_set(self, schema: CoreSchemaOrField) -> bool:
        return_value = super().field_title_should_be_set(schema)
        if return_value and is_core_schema(schema):
            return False
        return return_value

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], Any]]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, info: Any = None) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid objectid")
            return ObjectId(v)
        raise TypeError("PyObjectId must be provided as a valid ObjectId or its hex string")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type[Any], handler: Any) -> CoreSchema:
        base_schema = core_schema.any_schema()
        return core_schema.no_info_after_validator_function(
            cls.validate,
            base_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda obj: str(obj), info_arg=False
            )
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> dict[str, Any]:
        return {"$oid": {"type": "string"}}


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

class MongoDate(datetime):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type[Any], handler: Any) -> core_schema.CoreSchema:
        # Delegate to the standard datetime schema
        return core_schema.datetime_schema()

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> dict[str, Any]:
        # Return the Extended JSON representation for dates:
        return {"$date": {"type": "string", "format": "date-time"}}
