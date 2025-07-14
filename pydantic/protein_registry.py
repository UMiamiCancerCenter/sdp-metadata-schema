import json

from utils import (
    CustomBaseModel,
    GenerateJsonSchemaWithoutDefaultTitles,
    Scope,
    delete_empty_default,
)

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema


class GoTerm(CustomBaseModel):
    go_id: str = Field(..., description="GO term CURIE (e.g., GO:0005515)")  
    label: str = Field(..., description="Human-readable GO term label (e.g., 'protein binding')")

class GOAnnotations(CustomBaseModel):
    molecular_function: list[GoTerm] | SkipJsonSchema[None] = Field(None, description="List of molecular function GO terms")
    biological_process: list[GoTerm] | SkipJsonSchema[None] = Field(None, description="List of biological process GO terms")
    cellular_component: list[GoTerm] | SkipJsonSchema[None] = Field(None, description="List of cellular component GO terms")

class Xrefs(CustomBaseModel):
    refseq: str | SkipJsonSchema[None] = Field(None, title="RefSeq", description="RefSeq protein identifier")
    ensembl: str | SkipJsonSchema[None] = Field(None, description="Ensembl protein or gene identifier")
    pdb: list[str] | SkipJsonSchema[None] = Field(None, title="Protein Data Bank", description="List of Protein Data Bank structure IDs")
    interpro: list[str] | SkipJsonSchema[None] = Field(None, title="InterPro", description="List of InterPro domain identifiers")
    lincs: str | SkipJsonSchema[None] = Field(None, title="LINCS", description="LINCS PR_LINCS identifier for this protein, if available")

class Protein(CustomBaseModel):
    name: str = Field(..., description="Canonical protein name (e.g., from UniProt recommended name)")
    scope: Scope
    uniprot_id: str = Field(..., description="UniProt accession identifier for this protein")
    organism: str = Field(..., description="Species name for this protein (e.g., Homo sapiens)")  
    sequence: str = Field(..., description="Amino acid sequence of the protein")  
    sequence_length: int | SkipJsonSchema[None] = Field(None, description="Length of the protein sequence in amino acids")  
    gene_symbol: str | SkipJsonSchema[None] = Field(None, description="Official HGNC gene symbol associated with this protein")  
    alternative_names: list[str] | SkipJsonSchema[None] = Field(None, description="List of alternative names or synonyms for the protein")  
    function: str | SkipJsonSchema[None] = Field(None, description="Description of the protein's biological function")  
    subcellular_locations: list[str] | SkipJsonSchema[None] = Field(None, description="List of known subcellular localizations for the protein")  
    number_of_isoforms: int | SkipJsonSchema[None] = Field(None, description="Number of isoforms associated with the protein")  
    structure_model: str | SkipJsonSchema[None] = Field(None, description="PDB or Alphafold model identifier or URL")  
    xrefs: Xrefs | SkipJsonSchema[None] = Field(None, title="Cross-references", description="Cross-references for the protein across external databases")  
    go_annotations: GOAnnotations | SkipJsonSchema[None] = Field(None, title="Gene Ontology Annotations", description="List of associated GO terms (function, process, component)")  

if __name__ == "__main__":
    json_schema=Protein.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/protein/protein.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
