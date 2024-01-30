
""" an example with branching choices """

import json
from typing import Literal, Union, List, Optional, TypeAlias
from enum import Enum

# import streamlit as st
from pydantic import BaseModel, Field, field_validator, ValidationError
# import streamlit_pydantic as sp

from pydantic.config import ConfigDict

class smallMolecule(BaseModel):
    
    model_config = ConfigDict(title="Small Molecule")

    name: str = Field(title="Small Molecule Name")
    duration: str
    concentration: str

class crispr(BaseModel):
    
    model_config = ConfigDict(title="CRISPR")

    name: str = Field(title="Target Gene")
    duration: str
    concentration: str

class rnai(BaseModel):

    model_config = ConfigDict(title="RNAi")
    
    name: str = Field(title="Target Sequence")
    duration: str
    concentration: str

class antibody(BaseModel):
    
    name: str = Field(title="Antibody Name")
    duration: str
    concentration: str

class proteinP(BaseModel):
    
    model_config = ConfigDict(title='Protein')

    name: str = Field(title="Protein Name")
    duration: str
    concentration: str

class infectiousAgent(BaseModel):
    
    model_config = ConfigDict(title="Infectious Agent")

    name: str = Field(title="Agent Name")
    duration: str
    concentration: str

class epigeneticModification(BaseModel):

    model_config = ConfigDict(title="Epigenetic Modification")
    
    name: str = Field(title="Modification Type")
    entity: str = Field(default="Epigenetic Modification", 
                        json_schema_extra={"const": "Epigenetic Modification"})

class protein(BaseModel):
    
    model_config = ConfigDict(title="Protein")

    name: str = Field(title="Protein Name")
    entity: str = Field(default="Protein", json_schema_extra={"const": "Protein"})
class transcript(BaseModel):
    
    model_config = ConfigDict(title="Transcript")

    name: str = Field(title="NCBI Accession Number")
    entity: str = Field(default="Transcript", json_schema_extra={"const": "Transcript"})
class gene(BaseModel):
    
    model_config = ConfigDict(title="Gene")

    name: str = Field(title="Gene Name")
    entity: str = Field(default="Gene", json_schema_extra={"const": "Gene"})
class tissue(BaseModel):
    
    model_config = ConfigDict(title="Tissue")
    
    name: str = Field(title="Tissue Type")
    entity: str = Field(default="Tissue", json_schema_extra={"const": "Tissue"})

class primaryCells(BaseModel):

    model_config = ConfigDict(title="Primary Cells")
    
    name: str = Field(title="Cell Type")
    entity: str = Field(default="Primary Cells", 
                        json_schema_extra={"const": "Primary Cells"})

class differentiatedCells(BaseModel):
    
    model_config = ConfigDict(title="Differentiated Cells")

    name: str = Field(title="Cell Type")
    entity: str = Field(default="Differentiated Cells", 
                        json_schema_extra={"const": "Differentiated Cells"})

class ipsc(BaseModel):
    
    model_config = ConfigDict(title="iPSC")

    name: str = Field(title="iPSC ID")
    entity: str = Field(default="iPSC", json_schema_extra={"const": "iPSC"})

class cellLine(BaseModel):

    model_config = ConfigDict(title="Cell Line")
    
    name: str = Field(title="Cell Line Name")
    entity: str = Field(default="Cell Line", json_schema_extra={"const": "Cell Line"})

class wastewater(BaseModel):
    
    model_config = ConfigDict(title="Wastewater")

    name: str = Field(title="Sample ID")
    entity: str = Field(default="Wastewater", json_schema_extra={"const": "Wastewater"})
class patientSample(BaseModel):
    
    model_config = ConfigDict(title="Patient Sample")

    name: str = Field(title="Tumor Type")
    entity: str = Field(default="Patient Sample", 
                        json_schema_extra={"const": "Patient Sample"})
class target(BaseModel):
    
    model_config = ConfigDict(title="Molecular Target")
    entity: str = Field(default="Molecular Target", 
                                         json_schema_extra={"const": "Molecular Target"})

    content: Union[
            gene,
            transcript,
            protein,
            epigeneticModification
            ]


class biospecimen(BaseModel):
    
    model_config = ConfigDict(title="Biospecimen")
    entity: str = Field(default="Biospecimen", json_schema_extra={"const": "Biospecimen"})

    content: Union[
            patientSample,
            wastewater
            ]
    

class modelSystem(BaseModel):

    model_config = ConfigDict(title="Model System")
    entity: str = Field(default="Model System", 
                                         json_schema_extra={"const": "Model System"})

    content: Union[
            cellLine,
            ipsc,
            primaryCells,
            differentiatedCells,
            tissue
            ]

class sample(BaseModel):
    
    sampleName: str = Field(title='Sample Name')
    description: str
    experimentalSubject: Union[
            modelSystem,
            biospecimen,
            target
            ] = Field(title="Experimental Subject")

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