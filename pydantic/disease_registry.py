import json

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    Scope,
    delete_empty_default,
    to_title_case,
)

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema


class Xrefs(CustomBaseModel):
    mondo: str | SkipJsonSchema[None] = Field(None, description="MONDO identifier", title="MONDO")
    doid: str | SkipJsonSchema[None] = Field(None, description="Disease Ontology ID", title="Disease Ontology")
    omim: str | SkipJsonSchema[None] = Field(None, description="OMIM identifier", title="OMIM")
    orphanet: str | SkipJsonSchema[None] = Field(None, description="Orphanet registry ID")
    icd10: str | SkipJsonSchema[None] = Field(None, description="ICD‑10 classification code", title="ICD-10")
    umls: str | SkipJsonSchema[None] = Field(None, description="UMLS Concept Unique Identifier", title="UMLS")
    hpo: list[str] | SkipJsonSchema[None] = Field(None, description="List of HPO IDs associated with this disease", title="Human Phenotype Ontology")


class Disease(CustomBaseModel):

    name: str = Field(..., description="Preferred name of the disease")
    scope: Scope = Field(..., description="Scope of visibility or usage for this disease")
    synonyms: list[str] | SkipJsonSchema[None] = Field(None, description="Alternative names")
    definition: str | SkipJsonSchema[None] = Field(None, description="Official textual definition")
    xrefs: Xrefs | SkipJsonSchema[None] = Field(None, description="Cross-references to major disease ontologies", title="Cross-references")
    associated_genes: list[str] | SkipJsonSchema[None] = Field(None, description="Symbols for genes or proteins linked to this disease")
    phenotypes: list[str] | SkipJsonSchema[None] = Field(None, description="HPO term CURIE list describing observed phenotypes")
    inheritance_mode: str | SkipJsonSchema[None] = Field(None, description="Genetic inheritance model (e.g., AD, AR)")

if __name__ == "__main__":
    json_schema=Disease.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/disease/disease.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
