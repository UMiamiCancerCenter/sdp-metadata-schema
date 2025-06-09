import json
from typing import Any, Literal

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    MongoDate,
    PyObjectId,
    delete_empty_default,
)

from pydantic import ConfigDict, Field, model_validator
from pydantic.json_schema import SkipJsonSchema


class CrisprKnockout(CustomBaseModel):
    model_config = ConfigDict(title="CRISPR Knockout Registry", json_schema_extra={"version": "0.0.29"})

    id: PyObjectId | SkipJsonSchema[None] = Field(default_factory=PyObjectId)
    name: str
    scope: str = Field(..., alias="scope")
    alternative_names: list[str] | SkipJsonSchema[None] = Field(default=None, alias="alternativeNames")
    alternative_ids: list[str] | SkipJsonSchema[None] = Field(default=None, alias="alternativeIds")
    center_name: str | SkipJsonSchema[None] = Field(default=None, alias="centerName")
    center_canonical_id: str | SkipJsonSchema[None] = Field(default=None, alias="centerCanonicalId")
    provider_name: str | SkipJsonSchema[None] = Field(default=None, alias="providerName")
    provider_catalog_id: str | SkipJsonSchema[None] = Field(default=None, alias="providerCatalogId")
    lincs_id: str | SkipJsonSchema[None] = Field(default=None, alias="lincsId")
    is_coding: Literal["Coding", "Non-coding"] | SkipJsonSchema[None] = Field(default=None, alias="isCoding")
    target_locus: str | SkipJsonSchema[None] = Field(default=None, alias="targetLocus")
    target_locus_species: str | SkipJsonSchema[None] = Field(default=None, alias="targetLocusSpecies")
    target_gene_id: str | SkipJsonSchema[None] = Field(default=None, alias="targetGeneId")
    transcript_id: str | SkipJsonSchema[None] = Field(default=None, alias="tanscriptId")
    sense_sequence: str | SkipJsonSchema[None] = Field(default=None, alias="senseSequence")
    created_at: MongoDate | SkipJsonSchema[None] = Field(default=None, alias="createdAt")

    @model_validator(mode="before")
    @classmethod
    def rename_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values:
            values["id"] = values.pop("_id")
        return values

if __name__ == "__main__":
    json_schema=CrisprKnockout.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/crispr_knockout/crispr_knockout.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)