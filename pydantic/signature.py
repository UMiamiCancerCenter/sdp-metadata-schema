import json
from typing import Literal, Any

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from pydantic._internal._core_utils import is_core_schema, CoreSchemaOrField
from pydantic.json_schema import GenerateJsonSchema, SkipJsonSchema

def delete_empty_default(schema):
    for key in list(schema):
        if key == "default":
            if schema["default"] is None:
                schema.pop("default")
                continue
        if key == "oid":
            schema["$oid"] = schema.pop("oid")
            key = "$oid"
        if isinstance(schema[key], dict):
            delete_empty_default(schema[key])

class GenerateJsonSchemaWithoutDefaultTitles(GenerateJsonSchema):
    def field_title_should_be_set(self, schema: CoreSchemaOrField) -> bool:
        return_value = super().field_title_should_be_set(schema)
        if return_value and is_core_schema(schema):
            return False
        return return_value

class Perturbation(BaseModel):
    name: str = Field(title="Name")
    id: str | SkipJsonSchema[None] = Field(default=None, title="ID")
    type: Literal["Small Molecule", "CRISPR Knockout", "Protein", "Tet Expression System"] = Field(title="Perturbation Type")
    concentration: float | SkipJsonSchema[None] = Field(default=None, title="Concentration")
    concentrationUnits: str | SkipJsonSchema[None] = Field(default=None, title="Concentration Units")
    duration: float | SkipJsonSchema[None] = Field(default=None, title="Duration")
    durationUnits: str | SkipJsonSchema[None] = Field(default=None, title="Duration Units")

class Sample(BaseModel):
    name: str = Field(title="Sample Name", description="Name for this sample.")
    description: str | SkipJsonSchema[None] = Field(default=None)
    id: str = Field(title="Sample ID", description="ID by which this sample is identified in the input data.")
    datasetName: str = Field(default=None, title="Dataset Name", description="Name of the dataset the sample was taken from.")

class SampleGroup(BaseModel):
    name: str = Field(title="Group Name", description="Name for this group of samples.")
    description: str | SkipJsonSchema[None] = Field(default=None)
    samples: list[Sample] = Field(title="Samples")
    
class Input(BaseModel):
    fileType: str = Field(default=None, title="File Type")
    sampleGroups: list[SampleGroup] = Field(title="Sample Groups") 

class Signature(BaseModel):
    model_config = ConfigDict(title="Signature", json_schema_extra={"version": "0.0.24"})

    name: str = Field(title="Name")
    signatureType: Literal["Transcriptional Consensus Signature", "Differential Gene Expression"] = Field(title="Signature Type", default="Transcriptional Consensus Signature")
    description: str | SkipJsonSchema[None] = Field(default=None, title="Description")
    assay: str = Field(title="Assay")
    source: str | SkipJsonSchema[None] = Field(default=None, title="Source")
    sourceLink: str | SkipJsonSchema[None] = Field(default=None, title="Source Link")
    project: str | SkipJsonSchema[None] = Field(default=None, title="Project")
    organization: str | SkipJsonSchema[None] = Field(default=None, title="Organization")
    level: Literal[1, 2, 3, 4, 5, "Not Applicable"] = Field(title="Level")
    areaOfStudy: str | SkipJsonSchema[None] = Field(default=None, title="Area of Study")
    measuredEntity: str | SkipJsonSchema[None] = Field(default=None, title="Measured Entity")
    endpoints: list[Literal["log2FC", "TCS Score", "pIC50"]] = Field(title="Endpoint(s)")
    processingMethod: str | SkipJsonSchema[None] = Field(default=None, title="Processing Method")
    processingDescription: str | SkipJsonSchema[None] = Field(default=None, title="Processing Description")
    input: Input | SkipJsonSchema[None] = Field(default=None, title="Input", json_schema_extra={"type": "object"})
    experimentalSystems: list[Literal["Cell Line", "Primary Cell", "Tumor", "Tissue"]] = Field(title="Experimental Systems")
    perturbations: list[Perturbation] | SkipJsonSchema[None] = Field(default=None, title="Perturbations")
    data: Any = Field(default=None, title="Data", json_schema_extra={"format": "hidden", "type": "object"}) # Specific to what is submitted or pulled from external data source.


if __name__ == "__main__":
    json_schema=Signature.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("../json_schemas/signature/signature.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)