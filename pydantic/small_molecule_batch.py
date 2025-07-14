# ruff: noqa

import json

from bson import ObjectId as _ObjectId
from typing_extensions import Annotated  # noqa: UP035

from pydantic import BaseModel, Field
from pydantic._internal._core_utils import CoreSchemaOrField, is_core_schema
from pydantic.config import ConfigDict
from pydantic.functional_validators import AfterValidator
from pydantic.json_schema import GenerateJsonSchema


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return value

ObjectId = Annotated[str, AfterValidator(check_object_id)]

def delete_empty_default(schema):
    for key in list(schema):
        if key == "default" and schema["default"] == "":
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

class SmallMoleculeBatch(BaseModel):
    model_config = ConfigDict(title="Small Molecule Batch Fields")

    smallMoleculeLabBatchLabel: str = Field(title="Lab Batch Label",
                                             description="Lab-specific ID for the batch of small molecule used in the experiment.", default="")

    smallMoleculeSmilesBatch: str = Field(title="Small Molecule Vendor-provided SMILES", description="SMILES representation only as provided from the vendor; full structure with all information, i.e. isomeric SMILES", default="")

    smallMoleculeProviderName: str = Field(title="Small Molecule Provider Name", description="Vendor or lab that supplied the small molecule", default="")

    smallMoleculeProviderCatalogId: str = Field(title="Small Molecule Provider Catalog ID", description="ID or catalogue number assigned by the vendor or provider to the small molecule", default="")

    smallMoleculeProviderBatchId: str = Field(title="Small Molecule Vendor-provided SMILES", description="SMILES representation only as provided from the vendor; full structure with all information, i.e. isomeric SMILES", default="")

class SmallMoleculeCanonical(BaseModel):
    model_config = ConfigDict(title="Small Molecule Canonical Fields")

    smallMoleculeName: str = Field(title="Small Molecule Name", description="The common, primary, recognizable name for the small molecule being used.")

    smallMoleculeAlternativeNames: list[str] = Field(title="Small Molecule Alternative Names", description="List of synonymous compound names, drug name (if applicable), and other alternative names", default="")

    # smallMoleculeLabName: str = Field(title="Lab Name", description="Name of the lab running the experiment", default="")

    smallMoleculeLabCanonicalId: str = Field(title="Small Molecule Lab Canonical ID", description="Lab-specific ID for the small molecule compound", default="", json_schema_extra={"format": "hidden"})

    smallMoleculeLincsId: str = Field(title="Small Molecule LINCS ID", description="The global LINCS ID of the small molecule for cross-reference to the LINCS project", default="")

    smallMoleculePubChemCid: str = Field(title="Small Molecule PubChem CID", description="CID that corresponds to the standardized parent compound in NCBIs PubChem database", default="")

    smallMoleculeChebiId: str = Field(title="Small Molecule ChEBI ID", description="ChEBI ID of the small molecule", default="")

    smallMoleculeSmilesParent: str = Field(title="Small Molecule Canonical SMILES", description="Canonical isomeric SMILES representation of parent (standardized) chemical structure", default="")

class SmallMolecule(BaseModel):

    model_config = ConfigDict(title="Small Molecule Batch", 
                              description="Molecules with a low molecular weight (generally < 900 daltons) used to perturb the experimental system, often binding to specific biological targets.", arbitrary_types_allowed=True, json_schema_extra={
                        "version": "0.1.0"})

    name: str = Field(title="Small Molecule Batch Name", 
                                   description="Name for the batch of small molecule used in the experiment.")

    description: str = Field(default="", title="Description", 
                             description="Please include a description or any other helpful comments or annotations for the small molecule.")

    batchType: str = Field(default="Small Molecule", 
                                         json_schema_extra={"const": "Small Molecule", "format": "hidden"})

    scope: str = Field(default="private", json_schema_extra={"format": "hidden"})

    compoundId: ObjectId = Field(default="", description="A MongoDB ObjectId string", json_schema_extra={"format": "hidden"})

    batch: SmallMoleculeBatch = Field(default="")

    canonical: SmallMoleculeCanonical = Field(default="")

def main():
    json_schema=SmallMolecule.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("small_molecule_batch.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)

if __name__ == "__main__":
    main()
