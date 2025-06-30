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


class Antibody(CustomBaseModel):
    name: str = Field(..., description="Antibody name according to the vendor or provider")
    scope: Scope = Field(default=Scope.PUBLIC, description="Scope of visibility")
    lincs_id: str | SkipJsonSchema[None] = Field(None, title="LINCS ID", description="Global LINCS antibody ID (batch-independent)")
    relevant_citations: list[str] | SkipJsonSchema[None] = Field(None, description="PMIDs or patent numbers")
    rrid: str | SkipJsonSchema[None] = Field(None, title="RRID", description="Resource Identification Initiative ID (RRID) from antibodyregistry.org")
    clone_name: str | SkipJsonSchema[None] = Field(None, description="Monoclonal clone name or ID")
    antibody_type: str | SkipJsonSchema[None] = Field(None, description="Natural or engineered")
    target_protein: str = Field(..., description="Nominal protein target (UniProt name)")
    target_protein_id: str | SkipJsonSchema[None] = Field(None, title="Target Protein ID", description="UniProt ID of the protein target")
    non_protein_target: str | SkipJsonSchema[None] = Field(None, title="Non-protein Target", description="Name of the nominal target if not a protein")
    target_organism: str | SkipJsonSchema[None] = Field(None, description="Organism of the antibody target (NCBI Taxon)")
    immunogen: str | SkipJsonSchema[None] = Field(None, description="Description of the immunogen/entity used to generate the antibody")
    immunogen_sequence: str | SkipJsonSchema[None] = Field(None, description="Complete amino acid sequence of the immunogen")
    antibody_species: str = Field(..., description="Organism or species the antibody was derived from")
    antibody_clonality: str | SkipJsonSchema[None] = Field(None, description="Monoclonal or polyclonal")
    antibody_isotype: str | SkipJsonSchema[None] = Field(None, description="Isotype of the Fc domain (e.g., IgG)")
    antibody_production_source_organism: str = Field(..., description="Organism or cell type used to produce the antibody")
    antibody_production_details: str | SkipJsonSchema[None] = Field(None, description="Details about antibody production method")
    antibody_labeling: str | SkipJsonSchema[None] = Field(None, description="Fluor or enzyme conjugated to the antibody")
    antibody_labeling_details: str | SkipJsonSchema[None] = Field(None, description="Details about the labeling/conjugation protocol")

if __name__ == "__main__":
    json_schema=Antibody.model_json_schema(schema_generator=GenerateJsonSchema)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/antibody/antibody.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)