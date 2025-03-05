import json
from enum import Enum

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from pydantic._internal._core_utils import is_core_schema, CoreSchemaOrField
from pydantic.json_schema import GenerateJsonSchema

def delete_empty_default(schema):
    for key in list(schema):
        if key == "default":
            if schema["default"] == "":
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

class Level(Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"

class ExperimentalSystemType(Enum):
    cellLine = "Cell Line"
    primaryCell = "Primary Cell"

class PerturbationType(Enum):
    smallMolecule = "Small Molecule"
    crisprKnockout = "CRISPR Knockout"
    protein = "Protein"
    tetExpressionSystem = "Tet Expression System"

class Perturbation(BaseModel):
    name: str = Field(title="Name")
    id: str = Field(title="ID")
    type: PerturbationType = Field(title="Perturbation Type")
    concentration: float = Field(default="", title="Concentration")
    concentrationUnits: str = Field(default="", title="Concentration Units")
    duration: float = Field(default="", title="Duration")
    durationUnits: str = Field(default="", title="Duration Units")

class ObjectId(BaseModel):
    oid: str = Field(default="")

class Input(BaseModel):
    datasetName: str = Field(default="", title="Dataset Name")
    fileType: str = Field(default="", title="File Type")
    endpoints: list[str] = Field(default="", title="Endpoints")
    sampleIds: list[ObjectId] = Field(default="", title="Sample IDs") # Specific to type of signature.

class ExperimentalSystem(BaseModel):
    name: str = Field(title="Name")
    id: str = Field(title="ID")
    type: ExperimentalSystemType = Field("Type")

class Datum(BaseModel):
    geneSymbol: str = Field(title="Gene Symbol")
    score: float = Field(title="Score")

class SignatureTcs(BaseModel):
    model_config = ConfigDict(title="Signature", json_schema_extra={"version": "0.0.23"})

    name: str = Field(title="Name")
    signatureClass: str = Field(title="Signature Class", default="Within-group/Background", json_schema_extra={"const": "Within-group/Background", "format": "hidden"})
    signatureType: str = Field(title="Signature Type", default="Transcriptional Consensus Signature", json_schema_extra={"const": "Transcriptional Consensus Signature", "format": "hidden"})
    description: str = Field(default="", title="Description")
    assay: str = Field(title="Assay")
    source: str = Field(default="", title="Source")
    sourceLink: str = Field(default="", title="Source Link")
    project: str = Field(default="", title="Project")
    organization: str = Field(default="", title="Organization")
    level: Level = Field(default="", title="Level")
    areaOfStudy: str = Field(default="", title="Area of Study")
    measuredEntity: str = Field(default="", title="Measured Entity")
    endpoints: str = Field(default="TCS Score", title="Endpoints", json_schema_extra={"const": "TCS Score", "format": "hidden"})
    processingMethod: str = Field(default="", title="Processing Method")
    processingDescription: str = Field(default="", title="Processing Description")
    input: Input = Field(default="", title="Input", json_schema_extra={"type": "object"}) # In this object, the sampleIds field is specific to type of signature.
    experimentalSystems: list[ExperimentalSystem] = Field(default="", title="Experimental Systems")
    perturbations: list[Perturbation] = Field(default="", title="Perturbations")
    data: list[Datum] = Field(default="", title="Data") # Specific to type of signature


if __name__ == "__main__":
    json_schema=SignatureTcs.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("signature_TCS.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)