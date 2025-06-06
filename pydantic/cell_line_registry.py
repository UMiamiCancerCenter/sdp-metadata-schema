import json
from typing import Any

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    MongoDate,
    PyObjectId,
    delete_empty_default,
)

from pydantic import ConfigDict, Field, model_validator
from pydantic.json_schema import SkipJsonSchema


class ResourceEntry(CustomBaseModel):
    accession: str | SkipJsonSchema[None] = None
    category: str | SkipJsonSchema[None] = None
    database: str | SkipJsonSchema[None] = None
    url: str | SkipJsonSchema[None] = None
    iri: str | SkipJsonSchema[None] = None
    label: str | SkipJsonSchema[None] = None



class CellLine(CustomBaseModel):
    model_config = ConfigDict(title="Cell Line Registry", json_schema_extra={"version": "0.0.28"})

    id: PyObjectId | SkipJsonSchema[None] = Field(default_factory=PyObjectId)
    name: str = Field(..., alias="name")
    synonyms: list[str] | SkipJsonSchema[None] = Field(default=None, alias="synonyms")
    cellosaurus_accession: str | SkipJsonSchema[None] = Field(default=None, alias="cellosaurusAccession")
    disease: list[ResourceEntry] | SkipJsonSchema[None] = Field(default=None, alias="disease")
    species: list[ResourceEntry] | SkipJsonSchema[None] = Field(default=None, alias="species")
    sex: str | SkipJsonSchema[None] = Field(default=None, alias="sex")
    age_at_sampling: str | SkipJsonSchema[None] = Field(default=None, alias="ageAtSampling")
    category: str | SkipJsonSchema[None] = Field(default=None, alias="category")
    cell_line_databases: list[ResourceEntry] | SkipJsonSchema[None] = Field(default=None, alias="cellLineDatabases")
    anatomy_cell_type_resources: list[ResourceEntry] | SkipJsonSchema[None] = Field(default=None, alias="anatomyCellTypeResources")
    created_at: MongoDate | SkipJsonSchema[None] = Field(default=None, alias="createdAt")
    scope: str = Field(..., alias="scope")

    @model_validator(mode="before")
    @classmethod
    def rename_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values:
            values["id"] = values.pop("_id")
        return values

if __name__ == "__main__":
    json_schema=CellLine.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/cell_line/cell_line.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
