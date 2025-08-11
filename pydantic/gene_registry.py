import json
from typing import Any

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    Scope,
    delete_empty_default,
)

from pydantic import ConfigDict, Field, model_validator
from pydantic.json_schema import SkipJsonSchema


class GoEntry(CustomBaseModel):
    evidence: str | SkipJsonSchema[None] = Field(default=None, title="Evidence")
    gocategory: str | SkipJsonSchema[None] = Field(default=None, title="GO Category")
    go_id: str | SkipJsonSchema[None] = Field(default=None, title="GO ID", alias="goId")
    qualifier: str | SkipJsonSchema[None] = Field(default=None, title="Qualifier")
    term: str | SkipJsonSchema[None] = Field(default=None, title="Term")

class GO(CustomBaseModel):
    BP: list[GoEntry] | SkipJsonSchema[None] = Field(default=None, title="Biological Process")
    CC: list[GoEntry] | SkipJsonSchema[None] = Field(default=None, title="Cellular Component")
    MF: list[GoEntry] | SkipJsonSchema[None] = Field(default=None, title="Molecular Function")

class LinkedTrait(CustomBaseModel):
    label: str | SkipJsonSchema[None] = Field(default=None, title="Label")
    trait_id: str | SkipJsonSchema[None] = Field(default=None, title="Trait ID", alias="traitId")
    url: str | SkipJsonSchema[None] = Field(default=None, title="URL")

class GWASAssociation(CustomBaseModel):
    rs_id: str | SkipJsonSchema[None] = Field(default=None, title="RefSeq ID", alias="rsId")
    risk_label: str | SkipJsonSchema[None] = Field(default=None, title="Risk Label", alias="riskLabel")
    p_value: int | SkipJsonSchema[None] = Field(default=None, title="p-Value", alias="pValue")
    p_value_exponent: int | SkipJsonSchema[None] = Field(default=None, title="p-Value Exponent", alias="pValueExponent")
    trait_name: str | SkipJsonSchema[None] = Field(default=None, title="Trait Name", alias="traitName")
    linked_traits: list[LinkedTrait] | SkipJsonSchema[None] = Field(default=None, title="Linked Traits", alias="linkedTraits")

class KeggEntry(CustomBaseModel):
    kegg_id: str | SkipJsonSchema[None] = Field(default=None, title="KEGG ID", alias="keggId")
    kegg_name: str | SkipJsonSchema[None] = Field(default=None, title="Name", alias="keggName")

class ReactomeEntry(CustomBaseModel):
    reactome_id: str | SkipJsonSchema[None] = Field(default=None, title="Reactome ID", alias="reactomeId")
    reactome_name: str | SkipJsonSchema[None] = Field(default=None, title="Name", alias="reactomeName")

class WikipediaStub(CustomBaseModel):
    url_stub: str | SkipJsonSchema[None] = Field(default=None, title="URL Stub", alias="urlStub")
class Gene(CustomBaseModel):
    model_config = ConfigDict(title="Gene Registry", json_schema_extra={"version": "0.1.9"})

    name: str = Field(title="Name")
    scope: Scope = Field(default=Scope.PRIVATE, title="Scope")
    summary: str | SkipJsonSchema[None] = Field(default=None, title="Summary")
    alias: list[str] | SkipJsonSchema[None] = Field(default=None, title="Aliases")
    HGNC: str | SkipJsonSchema[None] = Field(default=None)
    symbol: str | SkipJsonSchema[None] = Field(default=None, title="Gene Symbol")
    map_location: str | SkipJsonSchema[None] = Field(default=None, title="Map Location", alias="mapLocation")
    entrez_gene: str | SkipJsonSchema[None] = Field(default=None, title="Entrez Gene ID", alias="entrezGene")
    ensembl: str | SkipJsonSchema[None] = Field(default=None, title="Ensembl ID")
    other_names: list[str] | SkipJsonSchema[None] = Field(default=None, title="Other Names", alias="otherNames")
    taxid: int | SkipJsonSchema[None] = Field(default=None, title="Taxonomy ID")
    species: str = Field(title="Species")
    type_of_gene: str | SkipJsonSchema[None] = Field(default=None, title="Type of Gene", alias="typeOfGene")
    go: GO | SkipJsonSchema[None] = Field(default=None, title="Gene Ontology")
    kegg: list[KeggEntry] | SkipJsonSchema[None] = Field(default=None, title="KEGG")
    reactome: list[ReactomeEntry] | SkipJsonSchema[None] = Field(default=None, title="Reactome")
    gwas_associations: list[GWASAssociation] | SkipJsonSchema[None] = Field(default=None, title="GWAS Asssociations", alias="gwasAssociations")
    wikipedia: WikipediaStub | SkipJsonSchema[None] = Field(default=None, title="Wikipedia Reference")

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
