import json

from pydantic import BaseModel, Field

from pydantic.config import ConfigDict
from pydantic._internal._core_utils import is_core_schema, CoreSchemaOrField
from pydantic.json_schema import GenerateJsonSchema, SkipJsonSchema

def delete_empty_default(schema):
    for key in list(schema):
        if key == "default":
            if schema["default"] is None:
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

class UniChem(BaseModel):
    chebi: list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEBI", description="ChEBI is a freely available ontology of molecular entities focused on 'small' chemical compounds")  
    chembl: list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEMBL", description="A database of bioactive drug-like small molecules and bioactivities abstracted from the scientific literature.") 
    lincs: list[str] | SkipJsonSchema[None] = Field(default=None, title="LINCS", description="The LINCS DCIC facilitates and standardizes the information relevant to LINCS assays as described in http://www.lincsproject.org/data/data-standards/")
    pubchem: list[str] | SkipJsonSchema[None] = Field(default=None, title="PubChem", description="A database of normalized PubChem compounds (CIDs) from the PubChem Database.")
    drugbank: list[str] | SkipJsonSchema[None] = Field(default=None, title="DrugBank", description="A database that combines drug (i.e. chemical, pharmacological and pharmaceutical) data with drug target (i.e. sequence, structure, and pathway) information.")

class Content(BaseModel):
    name: str | SkipJsonSchema[None] = Field(default=None, title="Name")
    alternativeNames: list[str] | SkipJsonSchema[None] = Field(default=None, title="Alternative Names")
    alternativeIds: list[str] | SkipJsonSchema[None] = Field(default=None, title="Alternative IDs")
    pubchemCid: str | SkipJsonSchema[None] = Field(default=None, title="PubChem CID")
    chebiId: str | SkipJsonSchema[None] = Field(default=None, title="ChEBI ID")
    inchiCanonical: str | SkipJsonSchema[None] = Field(default=None, title="Canonical InChI", description="InChi representation of standardized chemical structure")
    smilesCanonical: str | SkipJsonSchema[None] = Field(default=None, title="Canonical SMILES", description="Canonical SMILES representation of standardized chemical structure")
class Lincs(BaseModel):
    id: str | SkipJsonSchema[None] = Field(default=None, title="LINCS ID")
    name: str | SkipJsonSchema[None] = Field(default=None, title="Name")
    alternativeNames: list[str] | SkipJsonSchema[None] = Field(default=None, title="Alternative Names")
    alternativeIds: list[str] | SkipJsonSchema[None] = Field(default=None, title="Alternative IDs")
    pubchemCid: str | SkipJsonSchema[None] = Field(default=None, title="PubChem CID")
    chebiId: list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEBI ID")
    inchiParent: str | SkipJsonSchema[None] = Field(default=None, title="Parent InChI")
    inchiKeyParent: str | SkipJsonSchema[None] = Field(defaut=None, title="Parent InChI Key")
    smilesParent: str | SkipJsonSchema[None] = Field(default=None, title="Parent SMILES")
class Efo(BaseModel):
    term: str | SkipJsonSchema[None] = Field(default=None, title="Term")
class ChemblDrugIndication(BaseModel):
    efo: list[Efo] | SkipJsonSchema[None] = Field(default=None, title="EFO", description="Experimental Factor Ontology")
class ChemblTargetComponent(BaseModel):
    uniprot: list[str] | SkipJsonSchema[None] = Field(default=None, title="UniProt")

class ChemblDrugMechanism(BaseModel):
    actionType: list[str] | SkipJsonSchema[None] = Field(default=None, title="Action Type")
    targetComponents: list[ChemblTargetComponent] | SkipJsonSchema[None] = Field(default=None, title="Target Components")
    targetName: list[str] | SkipJsonSchema[None] = Field(default=None, title="Target Name")
class ChemblMoleculeSynonym(BaseModel):
    moleculeSynonym: str | SkipJsonSchema[None] = Field(default=None, title="Molecule Synonym")
    synType: str | SkipJsonSchema[None] = Field(default=None, title="Synonym Type")
class Chembl(BaseModel):
    drugIndications: list[ChemblDrugIndication] | SkipJsonSchema[None] = Field(default=None, title="Drug Indications")
    drugMechanisms: list[ChemblDrugMechanism] | SkipJsonSchema[None] = Field(default=None, title="Drug Mechanisms")
    maxPhase: float | SkipJsonSchema[None] = Field(default=None, title="Maximum Phase", description="Maximum phase of development reached for the compound (4 = approved). Null where max phase has not yet been assigned.")
    moleculeSynonyms: list[ChemblMoleculeSynonym] | SkipJsonSchema[None] = Field(default=None, title="Molecule Synonyms")
    moleculeType: str | SkipJsonSchema[None] = Field(default=None, title="Molecule Type")
class PubChemIupac(BaseModel):
    systematic: str | SkipJsonSchema[None] = Field(default=None, title="Systematic")
class PubChemSmiles(BaseModel):
    canonical: str | SkipJsonSchema[None] = Field(default=None, title="Canonical")
class PubChem(BaseModel):
    cid: int = Field(title="CID")
    inchi: str | SkipJsonSchema[None] = Field(default=None, title="InChI")
    inchikey: str | SkipJsonSchema[None] = Field(default=None, title="InChI Key")  
    iupac: PubChemIupac | SkipJsonSchema[None] = Field(default=None, title="IUPAC", json_schema_extra={"type": "object"})
    molecularFormula: str | SkipJsonSchema[None] = Field(default=None, title="Molecular Formula")
    smiles: PubChemSmiles | SkipJsonSchema[None] = Field(default=None, title="SMILES", json_schema_extra={"type": "object"})
 
class SmallMolecule(BaseModel):
    model_config = ConfigDict(title="Small Molecule", json_schema_extra={"version": "0.0.22"})

    name: str = Field(title="Name")
    content: Content | SkipJsonSchema[None] = Field(default=None, title="User-submitted Content", json_schema_extra={"type": "object"})
    unichem: UniChem | SkipJsonSchema[None] = Field(default=None, title="UniChem Cross References", json_schema_extra={"type": "object"})
    lincs: Lincs | SkipJsonSchema[None] = Field(default=None, title="LINCS Metadata", json_schema_extra={"type": "object"})
    chembl: Chembl | SkipJsonSchema[None] = Field(default=None, title="ChEMBL", json_schema_extra={"type": "object"})
    pubchem: list[PubChem] | SkipJsonSchema[None] = Field(default=None, title="PubChem")

if __name__ == "__main__":
    json_schema=SmallMolecule.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("small_molecule_registry.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)