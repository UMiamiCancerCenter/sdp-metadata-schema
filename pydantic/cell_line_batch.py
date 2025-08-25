# ruff: noqa

import json

from pydantic import BaseModel, Field
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator
from pydantic.config import ConfigDict
from pydantic._internal._core_utils import is_core_schema, CoreSchemaOrField
from pydantic.json_schema import GenerateJsonSchema

from bson import ObjectId as _ObjectId

def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value

ObjectId = Annotated[str, AfterValidator(check_object_id)]

def delete_empty_default(schema):
    for key in list(schema):
        if key == "default":
            if schema["default"] == "":
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

class CellLineBatch(BaseModel):
    model_config = ConfigDict(title="Cell Line Batch Fields")

    cellLineLabBatchLabel: str = Field(title="Lab Batch Label", description="Lab-specific ID for the batch of cells used in the experiment", default="")

    cellLineProviderName: str = Field(title="Cell Line Provider Name", description="Vendor or lab that supplied the cell line.", default="")

    cellLineProviderCatalogId: str = Field(title="Cell Line Provider Catalog ID", description="ID or catalogue number assigned by the vendor or provider to the cell line", default="")

    cellLineProviderBatchId: str = Field(title="Cell Line Provider Batch ID", description="Batch number or lot number assigned to the cells supplied by the vendor or provider", default="")

class CellLineCanonical(BaseModel):
    model_config = ConfigDict(title="Cell Line Canonical Fields")

    cellLineName: str = Field(title="Cell Line Name", 
                              description="The cell line name as found in the Cell Line Ontology. Must be a child term of 'immortal cell line cell'.", json_schema_extra={"graphRestriction":  {"ontologies": ["obo:clo"],"classes": ["CLO:0000019"], "queryFields": ["label"], "includeSelf": True}} 
                              )
    
    cellLineAlternativeNames: list[str] = Field(title="Cell Line Alternative Names", description="Other relevant names/aliases", default="")

    cellLineLabCanonicalId: str = Field(title="Cell Line Lab Canonical ID", description="Lab-specific ID for the cell line", default="", json_schema_extra={"format": "hidden"})

    cellLineLincsId: str = Field(title="Cell Line LINCS ID", description="Unique LINCS internal identifier", default="")

    cellLineAlternativeIds: list[str] = Field(title="Cell Line Alternative IDs", description="This field specifies the CLO, if available, or other common ID for the cell line or, if derived from another line, the CLO or other ID for the parent cell line. The parent cell line ID must be propagated to all cell lines derived from that parent line unless a distinct CLO has been assigned to the derived line.", default="")

    cellLineTissue: str = Field(title="Tissue of Origin", 
                                description="Tissue from which the cell line was derived, with name chosen from NCI Thesaurus, Brenda Tissue Ontology, or UBERON. Must be a child term of 'Tissue (NCIT)', 'tissues, cell types, and enzyme sources (BTO), or tissue (UBERON)'.", json_schema_extra={"graphRestriction":  {"ontologies" : ["obo:ncit","obo:bto","obo:uberon"], "classes": ["NCIT:C12801","BTO:0000000","UBERON:0000479"], "queryFields": ["label"], "includeSelf": True}}
                                )
    
    cellLineCellType: str = Field(title="Cell Line Cell Type", description="Cell type from which the cell line was derived, described using a controlled vocabulary.")
    
    cellLineOrgan: str = Field(title="Organ of Origin", 
                               description="Organ from which the cell line was derived, with name chosen from NCI Thesaurus, UBERON, or FMA. Must be a child term of 'organ'.",default="",json_schema_extra={"graphRestriction":  {"ontologies":["obo:ncit","obo:fma","obo:uberon"],"classes": ["NCIT:C13018","FMA:67498","UBERON:0000062"],"queryFields": ["label"],"includeSelf": True}})
    
    cellLineSpecies: str = Field(title="Species of Origin", 
                                  description="Species from which the cell line was derived, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'.",json_schema_extra={"graphRestriction":  {"ontologies":["obo:ncbitaxon"],"classes": ["NCBITaxon:131567"],"queryFields": ["label"],"includeSelf": True}})
    
    cellLineDisease: str = Field(title="Disease", 
                                 description="If the cell line came from a diseased tissue, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the origin tissue or cells were not diseased.",
                                 default="",json_schema_extra={"graphRestriction":  {"ontologies": ["obo:doid"],"classes": ["DOID:4"],"queryFields": ["label"],"includeSelf": True
                                }})
    
    cellLineDonorSex: str = Field(title="Cell Line Donor Sex", description="The sex of the organism from which the cell line was obtained", default="")

    cellLineDonorEthnicity: str = Field(title="Cell Line Donor Ethnicity", description="If the cell line was obtained from a human, the ethnicity of the donor", default="")

    cellLineDonorAge: float = Field(title="Cell Line Donor Age", description="The age in years of the organism from which the cell line was obtained", default="")

    cellLineGeneticModification: str = Field(title="Cell Line Genetic Modification", description="This field specifies any stable constructs as well as any genetic modifications (mutations, translocations) introduced into this cell line (e.g. H2B-mCherry integrated at the AAVS1 Safe Harbor locus). Details of the procedures used to generate this line (e.g. CRISPR/Cas9-mediated transformation) should be described and appropriate citations provided in the Production Details field.", default="")

class CellLine(BaseModel):

    model_config = ConfigDict(title="Cell Line Batch", 
                              description="Immortalized (naturally or engineered), genetically uniform tissue cells able to reproduce indefinitely in standard culture conditions.", json_schema_extra={
                        "version": "0.1.12"}
                              )
    
    name: str = Field(title="Cell Line Batch Name", 
                              description="Name for the batch of cells used in the experiment.")
                              
    
    description: str = Field(default="", title="Description", 
                             description="Please include a description or any other helpful comments or annotations for the cell line.")

    batchType: str = Field(default="Cell Line", 
                                         json_schema_extra={"const": "Cell Line", "format": "hidden"})
    
    scope: str = Field(default="private", json_schema_extra={"format": "hidden"})
    
    cellLineId: ObjectId = Field(default="", description="A MongoDB ObjectId string", json_schema_extra={"format": "hidden"})
    
    batch: CellLineBatch = Field(default="")

    canonical: CellLineCanonical = Field(default="")

def main():
    json_schema=CellLine.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("cell_line_batch.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)

if __name__ == "__main__":
    main()