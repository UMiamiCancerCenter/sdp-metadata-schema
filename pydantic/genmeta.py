import json
from typing import Literal, Union, List, Optional, TypeAlias
from enum import Enum

# import streamlit as st
from pydantic import BaseModel, Field, field_validator, ValidationError
# import streamlit_pydantic as sp

from pydantic.config import ConfigDict

class smallMolecule(BaseModel):
    
    model_config = ConfigDict(title="Small Molecule")

    entity: str = Field(default="Small Molecule", 
                                         json_schema_extra={"const": "Small Molecule",
                                                            "format": "hidden"})
    name: str = Field(title="Small Molecule Name")
    duration: str
    concentration: str

class crispr(BaseModel):
    
    model_config = ConfigDict(title="CRISPR")

    entity: str = Field(default="CRISPR", 
                                         json_schema_extra={"const": "CRISPR",
                                                            "format": "hidden"})
    name: str = Field(title="Target Gene")
    duration: str
    concentration: str

class rnai(BaseModel):

    model_config = ConfigDict(title="RNAi")
    
    entity: str = Field(default="RNAi", 
                                         json_schema_extra={"const": "RNAi",
                                                            "format": "hidden"})
    name: str = Field(title="Target Sequence")
    duration: str
    concentration: str

class antibody(BaseModel):

    model_config = ConfigDict(title="Antibody")
    
    entity: str = Field(default="Antibody", 
                                         json_schema_extra={"const": "Antibody",
                                                            "format": "hidden"})
    name: str = Field(title="Antibody Name")
    duration: str
    concentration: str

class proteinP(BaseModel):
    
    model_config = ConfigDict(title='Protein')

    entity: str = Field(default="Protein", 
                                         json_schema_extra={"const": "Protein",
                                                            "format": "hidden"})
    name: str = Field(title="Protein Name")
    duration: str
    concentration: str

class infectiousAgent(BaseModel):
    
    model_config = ConfigDict(title="Infectious Agent")

    entity: str = Field(default="Infectious Agent", 
                                         json_schema_extra={"const": "Infectious Agent",
                                                            "format": "hidden"})
    name: str = Field(title="Agent Name")
    duration: str
    concentration: str

class epigeneticModification(BaseModel):

    model_config = ConfigDict(title="Epigenetic Modification")
    
    entity: str = Field(default="Epigenetic Modification", 
                        json_schema_extra={"const": "Epigenetic Modification",
                                           "format": "hidden"})
    name: str = Field(title="Modification Type")
    
class protein(BaseModel):
    
    model_config = ConfigDict(title="Protein")

    entity: str = Field(default="Protein", json_schema_extra={"const": "Protein",
                                                              "format": "hidden"})
    name: str = Field(title="Protein Name")
class transcript(BaseModel):
    
    model_config = ConfigDict(title="Transcript")

    entity: str = Field(default="Transcript", json_schema_extra={"const": "Transcript",
                                                                 "format": "hidden"})
    name: str = Field(title="NCBI Accession Number")
class gene(BaseModel):
    
    model_config = ConfigDict(title="Gene")

    entity: str = Field(default="Gene", json_schema_extra={"const": "Gene",
                                                           "format": "hidden"})
    name: str = Field(title="Gene Name")
class tissue(BaseModel):
    
    model_config = ConfigDict(title="Tissue")

    entity: str = Field(default="Tissue", json_schema_extra={"const": "Tissue",
                                                             "format": "hidden"})
    name: str = Field(title="Tissue Type")

class primaryCells(BaseModel):

    model_config = ConfigDict(title="Primary Cells")

    entity: str = Field(default="Primary Cells", 
                        json_schema_extra={"const": "Primary Cells",
                                           "format": "hidden"})
    name: str = Field(title="Cell Type")

class differentiatedCells(BaseModel):
    
    model_config = ConfigDict(title="Differentiated Cells")

    entity: str = Field(default="Differentiated Cells", 
                        json_schema_extra={"const": "Differentiated Cells",
                                           "format": "hidden"})
    name: str = Field(title="Cell Type")
class ipsc(BaseModel):
    
    model_config = ConfigDict(title="iPSC")

    entity: str = Field(default="iPSC", json_schema_extra={"const": "iPSC",
                                                           "format": "hidden"})
    name: str = Field(title="iPSC ID")

class cellLine(BaseModel):

    model_config = ConfigDict(title="Cell Line")

    entity: str = Field(default="Cell Line", json_schema_extra={"const": "Cell Line",
                                                                "format": "hidden"})
    name: str = Field(title="Cell Line Name")

class wastewater(BaseModel):
    
    model_config = ConfigDict(title="Wastewater")

    entity: str = Field(default="Wastewater", json_schema_extra={"const": "Wastewater",
                                                                 "format": "hidden"})
    name: str = Field(title="Sample ID")

class patientSample(BaseModel):
    
    model_config = ConfigDict(title="Patient Sample")

    entity: str = Field(default="Patient Sample", 
                        json_schema_extra={"const": "Patient Sample",
                                           "format": "hidden"})
    name: str = Field(title="Tumor Type")
   
class target(BaseModel):
    
    model_config = ConfigDict(title="Molecular Target")

    entity: str = Field(default="Molecular Target", 
                                         json_schema_extra={"const": "Molecular Target",
                                                            "format": "hidden"})
    content: Union[
            gene,
            transcript,
            protein,
            epigeneticModification
            ]


class biospecimen(BaseModel):
    
    model_config = ConfigDict(title="Biospecimen")

    entity: str = Field(default="Biospecimen", json_schema_extra={"const": "Biospecimen",
                                                                  "format": "hidden"})
    content: Union[
            patientSample,
            wastewater
            ]
    

class modelSystem(BaseModel):

    model_config = ConfigDict(title="Model System")
    
    entity: str = Field(default="Model System", 
                                         json_schema_extra={"const": "Model System",
                                                            "format": "hidden"})
    content: Union[
            cellLine,
            ipsc,
            primaryCells,
            differentiatedCells,
            tissue
            ]

class sample(BaseModel):

    model_config = ConfigDict(title="Sample")
    
    sampleName: str = Field(title='Sample Name')
    description: str
    experimentalSystem: Union[
            modelSystem,
            biospecimen,
            target
            ] = Field(title="Experimental System")
    perturbation: List[Union[
        smallMolecule,
        crispr,
        rnai,
        antibody,
        proteinP,
        infectiousAgent
            ] 
        ]
                 

def example():
    """ run this to see the schema dumped """
    with open ("genmeta_schema.json", "w") as ft:
        print(json.dumps(sample.model_json_schema(), indent=2), 
              file = ft)

example()

# data = sp.pydantic_form(key="my_form", model=ExperimentalSubject)
# if data:
#     st.json(data.json())