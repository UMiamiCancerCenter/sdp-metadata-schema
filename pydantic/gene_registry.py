import json
from typing import Any

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    PyObjectId,
    Scope,
    delete_empty_default,
)

from pydantic import ConfigDict, Field, model_validator
from pydantic.json_schema import SkipJsonSchema


class GoEntry(CustomBaseModel):
    evidence: str | SkipJsonSchema[None] = Field(default=None, title="Evidence")
    gocategory: str | SkipJsonSchema[None] = Field(default=None, title="GO Category")
    id: str | SkipJsonSchema[None] = Field(default=None, title="GO ID")
    qualifier: str | SkipJsonSchema[None] = Field(default=None, title="Qualifier")
    term: str | SkipJsonSchema[None] = Field(default=None, title="Term")

class GO(CustomBaseModel):
    BP: list[GoEntry] | SkipJsonSchema[None] = Field(default=None, title="Biological Process")
    CC: list[GoEntry] | SkipJsonSchema[None] = Field(default=None, title="Cellular Component")
    MF: list[GoEntry] | SkipJsonSchema[None] = Field(default=None, title="Molecular Function")

class LinkedTrait(CustomBaseModel):
    trait: str | SkipJsonSchema[None] = Field(default=None, title="Trait")
    uri: str | SkipJsonSchema[None] = Field(default=None, title="URI")
    short_form: str | SkipJsonSchema[None] = Field(default=None, title="Short Form", alias="shortForm")

class GWASAssociation(CustomBaseModel):
    rsId: str | SkipJsonSchema[None] = Field(default=None, title="RefSeq ID")
    functional_class: str | SkipJsonSchema[None] = Field(default=None, title="Functional Class", alias="functionalClass")
    linked_traits: list[LinkedTrait] | SkipJsonSchema[None] = Field(default=None, title="Linked Traits", alias="linkedTraits")

class Gene(CustomBaseModel):
    model_config = ConfigDict(title="Gene Registry", json_schema_extra={"version": "0.0.26"})

    id: PyObjectId = Field(default_factory=PyObjectId, title="Signature ID")
    name: str = Field(title="Name")
    scope: Scope = Field(default=Scope.PRIVATE, title="Scope")
    description: str | SkipJsonSchema[None] = Field(default=None, title="Description")
    HGNC: str | SkipJsonSchema[None] = Field(default=None)
    symbol: str | SkipJsonSchema[None] = Field(default=None, title="Gene Symbol")
    entrez_gene: str | SkipJsonSchema[None] = Field(default=None, title="Entrez Gene ID", alias="entrezGene")
    ensembl: str | SkipJsonSchema[None] = Field(default=None, title="Ensembl ID")
    other_names: list[str] | SkipJsonSchema[None] = Field(default=None, title="Other Names", alias="otherNames")
    taxid: int | SkipJsonSchema[None] = Field(default=None, title="Taxonomy ID")
    species: str = Field(title="Species")
    type_of_gene: str | SkipJsonSchema[None] = Field(default=None, title="Type of Gene", alias="typeOfGene")
    go: GO | SkipJsonSchema[None] = Field(default=None, title="Gene Ontology")
    gwas_associations: list[GWASAssociation] | SkipJsonSchema[None] = Field(default=None, title="GWAS Asssociations", alias="gwasAssociations")

    @model_validator(mode="before")
    @classmethod
    def rename_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values:
            values["id"] = values.pop("_id")
        return values

if __name__ == "__main__":
    json_schema=Gene.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/gene/gene.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
