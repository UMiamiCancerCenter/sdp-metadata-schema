
""" an example with branching choices """

import json
from typing import Literal, Union, List, Optional, TypeAlias
from enum import Enum

# import streamlit as st
from pydantic import BaseModel, Field, fields
# import streamlit_pydantic as sp

from pydantic.config import ConfigDict

class SmallMolecule(BaseModel):
    
    model_config = ConfigDict(title="Small Molecule")

    Name: str = Field(title="Small Molecule Name")
    Duration: str
    Concentration: str

class CRISPR(BaseModel):
    
    Name: str = Field(title="Target Gene")
    Duration: str
    Concentration: str

class RNAi(BaseModel):
    
    Name: str = Field(title="Target Sequence")
    Duration: str
    Concentration: str

class Antibody(BaseModel):
    
    Name: str = Field(title="Antibody Name")
    Duration: str
    Concentration: str

class ProteinP(BaseModel):
    
    model_config = ConfigDict(title='Protein')

    Name: str = Field(title="Protein Name")
    Duration: str
    Concentration: str

class InfectiousAgent(BaseModel):
    
    model_config = ConfigDict(title="Infectious Agent")

    Name: str = Field(title="Agent Name")
    Duration: str
    Concentration: str

class EpigeneticModification(BaseModel):

    model_config = ConfigDict(title="Epigenetic Modification")
    
    Name: str = Field(title="Modification Type")

class Protein(BaseModel):
    
    Name: str = Field(title="Protein Name")

class Transcript(BaseModel):
    
    Name: str = Field(title="NCBI Accession Number")

class Gene(BaseModel):
    
    Name: str = Field(title="Gene Name")

class Tissue(BaseModel):
    
    Name: str = Field(title="Tissue Type")

class PrimaryCells(BaseModel):

    model_config = ConfigDict(title="Primary Cells")
    
    Name: str = Field(title="Cell Type")

class DifferentiatedCells(BaseModel):
    
    model_config = ConfigDict(title="Differentiated Cells")

    Name: str = Field(title="Cell Type")

class iPSC(BaseModel):
    
    Name: str = Field(title="iPSC ID")

class CellLine(BaseModel):

    model_config = ConfigDict(title="Cell Line")
    
    Name: str = Field(title="Cell Line Name")

class Wastewater(BaseModel):
    
    Name: str = Field(title="Sample ID")

class PatientSample(BaseModel):
    
    model_config = ConfigDict(title="Patient Sample")

    Name: str = Field(title="Tumor Type")

class Target(BaseModel):
    
    type: Union[
            Gene,
            Transcript,
            Protein,
            EpigeneticModification
            ]


class Biospecimen(BaseModel):
    
    type: Union[
            PatientSample,
            Wastewater
            ]


class ModelSystem(BaseModel):

    model_config = ConfigDict(title="Model System")
   
    type: Union[
            CellLine,
            iPSC,
            DifferentiatedCells,
            PrimaryCells,
            Tissue
            ]


class Sample(BaseModel):
    
    SampleName: str = Field(title='Sample Name')
    Description: str
    ExperimentalSubject: Union[
            ModelSystem,
            Biospecimen,
            Target
            ] = Field(title="Experimental Subject")
    Perturbation: List[Union[
        SmallMolecule,
        CRISPR,
        RNAi,
        Antibody,
        ProteinP,
        InfectiousAgent
    ] 
        ]
                 

def example():
    """ run this to see the schema dumped """
    with open ("genmeta_schema.json", "w") as ft:
        print(json.dumps(Sample.model_json_schema(), indent=2), 
              file = ft)

example()

# data = sp.pydantic_form(key="my_form", model=ExperimentalSubject)
# if data:
#     st.json(data.json())