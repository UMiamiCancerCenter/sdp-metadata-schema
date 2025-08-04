import json
from typing import Any

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    PerturbationType,
    Scope,
    SignatureType,
    delete_empty_default,
)

from pydantic import ConfigDict, Field, model_validator
from pydantic.json_schema import SkipJsonSchema


class Perturbation(CustomBaseModel):

    name: str | SkipJsonSchema[None] = Field(default=None, title="Name")
    perturbation_id: str | SkipJsonSchema[None] = Field(default=None, title="ID", alias="perturbationId", json_schema_extra={"pattern": "^[a-fA-F0-9]{24}$"})
    type: PerturbationType = Field(title="Perturbation Type")
    concentration: float | SkipJsonSchema[None] = Field(default=None, title="Concentration")
    concentration_units: str | SkipJsonSchema[None] = Field(default=None, title="Concentration Units", alias="concentrationUnits")
    duration: float | SkipJsonSchema[None] = Field(default=None, title="Duration")
    duration_units: str | SkipJsonSchema[None] = Field(default=None, title="Duration Units", alias="durationUnits")

class ModelSystemItem(CustomBaseModel):
    name: str | SkipJsonSchema[None] = Field(default=None, title="Name")
    model_system_id: str | SkipJsonSchema[None] = Field(default=None, title="ID", alias="modelSystemId", json_schema_extra={"pattern": "^[a-fA-F0-9]{24}$"})

class ModelSystem(CustomBaseModel):

    type: str | SkipJsonSchema[None] = Field(default=None, title="Type")
    items: list[ModelSystemItem] | SkipJsonSchema[None] = Field(default=None, title="Model System Items")

class Sample(CustomBaseModel):

    name: str = Field(title="Sample Name", description="Name for this sample.")
    description: str | SkipJsonSchema[None] = Field(default=None)
    sample_id: str | SkipJsonSchema[None] = Field(default=None, title="Sample ID", description="ID by which this sample is identified in the input data.", alias="sampleId", json_schema_extra={"pattern": "^[a-fA-F0-9]{24}$"})
    dataset: str | SkipJsonSchema[None] = Field(default=None, title="Dataset Name or ID")

class SampleGroup(CustomBaseModel):
    name: str | SkipJsonSchema[None] = Field(default=None, title="Group Name", description="Name for this group of samples.")
    description: str | SkipJsonSchema[None] = Field(default=None)
    samples: list[Sample] | SkipJsonSchema[None] = Field(default=None, title="Samples")
    model_systems: list[ModelSystem] | SkipJsonSchema[None] = Field(default=None, title="Model Systems", alias="modelSystems")
    perturbations: list[Perturbation] | SkipJsonSchema[None] = Field(default=None, title="Perturbations")

class Analytes(CustomBaseModel):
    type: str | SkipJsonSchema[None]= Field(default=None, title="Type")
    items: tuple[str, ...] | str | SkipJsonSchema[None] = Field(default=None, title="Analyte(s)", description="List of analyte names, or a single ObjectId string pointing to the list.")

class Signature(CustomBaseModel):
    model_config = ConfigDict(title="Signature", json_schema_extra={"version": "0.1.6"})

    name: str = Field(title="Name")
    scope: Scope = Field(default=Scope.PRIVATE, title="Scope", alias="scope")
    signature_type: SignatureType = Field(title="Signature Type", alias="signatureType")
    description: str | SkipJsonSchema[None] = Field(default=None, title="Description")
    source: str | SkipJsonSchema[None] = Field(default=None, title="Source")
    source_link: str | SkipJsonSchema[None] = Field(default=None, title="Source Link", alias="sourceLink")
    project: str | SkipJsonSchema[None] = Field(default=None, title="Project")
    organization: str | SkipJsonSchema[None] = Field(default=None, title="Organization")
    sample_groups: list[SampleGroup] | SkipJsonSchema[None] = Field(default=None, title="Input", alias="sampleGroups")
    area_of_study: str | SkipJsonSchema[None] = Field(default=None, title="Area of Study", alias="areaOfStudy")
    assay: str | SkipJsonSchema[None] = Field(default=None, title="Assay")
    analytes: list[Analytes] = Field(title="Analyte(s)")
    method: str = Field(title="Processing Method")
    endpoints: list[str] = Field(title="Endpoint(s)")
    data: list[Any] | SkipJsonSchema[None] = Field(default=None, title="Data")

    @model_validator(mode="before")
    @classmethod
    def rename_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values:
            values["id"] = values.pop("_id")
        return values

if __name__ == "__main__":
    json_schema=Signature.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/signature/signature.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
