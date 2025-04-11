import json
from typing import Any, Self

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    PyObjectId,
    delete_empty_default,
)

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.json_schema import SkipJsonSchema


class Content(CustomBaseModel):
    name: str | SkipJsonSchema[None] = None
    alternative_names: list[str] | SkipJsonSchema[None] = Field(default=None, alias="alternativeNames")
    alternative_ids: list[str] | SkipJsonSchema[None] = Field(default=None, alias="alternativeIds")
    pubchem_cid: int | SkipJsonSchema[None] = Field(default=None, alias="pubchemCid")
    chebi_id: str | SkipJsonSchema[None] = Field(default=None, alias="chebiId")
    inchi_canonical: str | SkipJsonSchema[None] = Field(default=None, alias="inchiCanonical")
    smiles_canonical: str | SkipJsonSchema[None] = Field(default=None, alias="smilesCanonical")

class UniChem(CustomBaseModel):
    chebi: str | list[str] | SkipJsonSchema[None] = None
    chembl: str | list[str] | SkipJsonSchema[None] = None
    lincs: str | list[str] | SkipJsonSchema[None] = None
    pubchem: int | list[int] | SkipJsonSchema[None] = None
    drugbank: str | list[str] | SkipJsonSchema[None] = None

    @field_validator("chebi", "chembl", "lincs", "drugbank", mode="before")
    @classmethod
    def ensure_list(cls: type[Self], v: Any) -> list[Any] | SkipJsonSchema[None]:
        if v is None:
            return v
        if isinstance(v, list):
            return v
        return [v]

    @field_validator("pubchem", mode="before")
    @classmethod
    def ensure_list_pubchem(cls: type[Self], v: Any) -> list[Any] | SkipJsonSchema[None]:
        if v is None:
            return v
        if isinstance(v, list):
            return v
        return [v]

class Lincs(CustomBaseModel):
    id: str
    name: str | SkipJsonSchema[None] = None
    alternative_names: list[str] | SkipJsonSchema[None] = Field(default=None, alias="alternativeNames")
    alternative_ids: list[str] | SkipJsonSchema[None] = Field(default=None, alias="alternativeIds")
    pubchem_cid: int | SkipJsonSchema[None] = Field(default=None, alias="pubchemCid")
    chebi_id: list[int] | SkipJsonSchema[None] = Field(default=None, alias="chebiId")
    inchi_parent: str | SkipJsonSchema[None] = Field(default=None, alias="inchiParent")
    inchi_key_parent: str | SkipJsonSchema[None] = Field(default=None, alias="inchiKeyParent")
    smiles_parent: str | SkipJsonSchema[None] = Field(default=None, alias="smilesParent")

class Efo(CustomBaseModel):
    term: str | SkipJsonSchema[None] = None

class ChemblDrugIndication(CustomBaseModel):
    efo: list[Efo] | SkipJsonSchema[None] = None

class ChemblTargetComponent(CustomBaseModel):
    uniprot: list[str] | SkipJsonSchema[None] = None

class ChemblDrugMechanism(CustomBaseModel):
    action_type: list[str] | SkipJsonSchema[None] = Field(default=None, alias="actionType")
    target_components: list[ChemblTargetComponent] | SkipJsonSchema[None] = Field(default=None, alias="targetComponents")
    target_name: list[str] | SkipJsonSchema[None] = Field(default=None, alias="targetName")

class ChemblMoleculeSynonym(CustomBaseModel):
    molecule_synonym: str | SkipJsonSchema[None] = Field(default=None, alias="moleculeSynonym")
    syn_type: str | SkipJsonSchema[None] = Field(default=None, alias="synType")

class Chembl(CustomBaseModel):
    drug_indications: list[ChemblDrugIndication] | SkipJsonSchema[None] = Field(default=None, alias="drugIndications")
    drug_mechanisms: list[ChemblDrugMechanism] | SkipJsonSchema[None] = Field(default= None, alias="drugMechanisms")
    max_phase: float | SkipJsonSchema[None] = Field(default=None, alias="maxPhase")
    molecule_synonyms: list[ChemblMoleculeSynonym] | SkipJsonSchema[None] = Field(default=None, alias="moleculeSynonyms")
    molecule_type: str | SkipJsonSchema[None] = Field(default=None, alias="moleculeType")

class PubChemIupac(CustomBaseModel):
    systematic: str | SkipJsonSchema[None] = None

class PubChemSmiles(CustomBaseModel):
    canonical: str | SkipJsonSchema[None] = None

class PubChem(CustomBaseModel):
    cid: int
    inchi: str | SkipJsonSchema[None] = None
    inchikey: str | SkipJsonSchema[None] = None
    iupac: PubChemIupac | SkipJsonSchema[None] = None
    molecular_formula: str | SkipJsonSchema[None] = Field(default=None, alias="molecularFormula")
    smiles: PubChemSmiles | SkipJsonSchema[None] = None

class SmallMolecule(CustomBaseModel):
    model_config = ConfigDict(title="Small Molecule Registry", json_schema_extra={"version": "0.0.25"})

    id:  PyObjectId | SkipJsonSchema[None] = Field(default_factory=PyObjectId)
    name: str
    scope: str
    content: Content | SkipJsonSchema[None] = None
    unichem: UniChem | SkipJsonSchema[None] = None
    lincs: Lincs | SkipJsonSchema[None] = None
    chembl: Chembl | SkipJsonSchema[None] = None
    pubchem: list[PubChem] | SkipJsonSchema[None] = None
    structure_image: str | SkipJsonSchema[None] = Field(default=None, alias="structureImage")

    @model_validator(mode="before")
    @classmethod
    def rename_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values:
            values["id"] = values.pop("_id")
        return values

if __name__ == "__main__":
    json_schema=SmallMolecule.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/small_molecule/small_molecule_registry.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
