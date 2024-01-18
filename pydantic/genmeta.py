
""" an example with branching choices """

import json
from typing import Literal, Union, List, Optional, TypeAlias
from enum import Enum

# import streamlit as st
from pydantic import BaseModel, Field, fields
# import streamlit_pydantic as sp

from pydantic.config import ConfigDict

class smallMolecule(BaseModel):
    
    model_config = ConfigDict(title="Small Molecule")

    name: str = Field(default="JQ1", title="Small Molecule Name")
    duration: str = Field(default="0 hrs")
    concentration: str = Field(default="μM")

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

class protein(BaseModel):
    
    name: str = Field(title="Protein Name")

class transcript(BaseModel):
    
    name: str = Field(title="NCBI Accession Number")

class gene(BaseModel):
    
    name: str = Field(title="Gene Name")

class tissue(BaseModel):
    
    name: str = Field(title="Tissue Type")

class primaryCells(BaseModel):

    model_config = ConfigDict(title="Primary Cells")
    
    name: str = Field(title="Cell Type")

class differentiatedCells(BaseModel):
    
    model_config = ConfigDict(title="Differentiated Cells")

    name: str = Field(title="Cell Type")

class ipsc(BaseModel):
    
    model_config = ConfigDict(title="iPSC")

    name: str = Field(title="iPSC ID")

class cellLine(BaseModel):

    model_config = ConfigDict(title="Cell Line")
    
    name: str = Field(default = "MCF7 cell", title="Cell Line Name")
    experimentalSubjectType: str = Field(default="Cell Line", 
                                         json_schema_extra={"const": "Cell Line"})

class wastewater(BaseModel):
    
    name: str = Field(title="Sample ID")

class patientSample(BaseModel):
    
    model_config = ConfigDict(title="Patient Sample")

    name: str = Field(title="Tumor Type")

class target(BaseModel):
    
    model_config = ConfigDict(title="Molecular Target")

    type: Union[
            gene,
            transcript,
            protein,
            epigeneticModification
            ]


class biospecimen(BaseModel):
    
    model_config = ConfigDict(title="Biospecimen")

    type: Union[
            patientSample,
            wastewater
            ]


class modelSystem(BaseModel):

    model_config = ConfigDict(title="Model System")
   
    type: Union[
            cellLine,
            ipsc,
            differentiatedCells,
            primaryCells,
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