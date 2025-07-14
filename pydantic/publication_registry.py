import json
from datetime import date

from utils import (
    CustomBaseModel,
    Scope,
    delete_empty_default,
)

from pydantic import (
    Field,
)
from pydantic.json_schema import GenerateJsonSchema, SkipJsonSchema


class Author(CustomBaseModel):
    name: str = Field(..., description="Full name or group author")
    orcid: str | SkipJsonSchema[None] = Field(None, title="ORCID ID", description="ORCID identifier for author")

class Xrefs(CustomBaseModel):
    doi: str | SkipJsonSchema[None] = Field(None, title="DOI", description="Digital Object Identifier")
    pmid: str | SkipJsonSchema[None] = Field(None, title="PubMed ID", description="PubMed ID")
    pmcid: str | SkipJsonSchema[None] = Field(None, title="PubMed Central ID", description="PubMed Central ID")
    arxiv: str | SkipJsonSchema[None] = Field(None, title="arXiv ID", description="arXiv ID")
    issn_print: str | SkipJsonSchema[None] = Field(None, title="ISSN Print", description="ISSN (print version)")
    issn_electronic: str | SkipJsonSchema[None] = Field(None, title="ISSN Electronic", description="ISSN (electronic version)")
    isbn: list[str] | SkipJsonSchema[None] = Field(None, title="ISBN", description="ISBNs")
    url: str | SkipJsonSchema[None] = Field(None, title="URL", description="Article or publisher URL")

class Publication(CustomBaseModel):
    scope: Scope = Field(..., description="Scope of visibility or usage for this publication")
    xrefs: Xrefs | SkipJsonSchema[None] = Field(default=None, title="Cross-references")
    title: str = Field(..., description="Full title of the publication")
    authors: list[Author] = Field(..., description="List of authors")
    journal: str | SkipJsonSchema[None] = Field(None, description="Name of journal or venue")
    publication_date: date = Field(..., description="Publication date in ISO format")
    volume: str | SkipJsonSchema[None] = Field(None, description="Journal volume")
    issue: str | SkipJsonSchema[None] = Field(None, description="Journal issue")
    pages: str | SkipJsonSchema[None] = Field(None, description="Page range")
    abstract: str | SkipJsonSchema[None] = Field(None, description="Abstract or summary text")
    keywords: list[str] | SkipJsonSchema[None] = Field(None, description="Author-supplied keywords")
    mesh_headings: list[str] | SkipJsonSchema[None] = Field(None, description="MeSH (Medical Subject Headings) terms from PubMed or curation")
    cited_by: list[str] | SkipJsonSchema[None] = Field(None, description="PMIDs of citing publications")

if __name__ == "__main__":
    json_schema=Publication.model_json_schema(schema_generator=GenerateJsonSchema)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/publication/publication.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
