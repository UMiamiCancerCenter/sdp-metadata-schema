
""" an example with branching choices """

import json
from typing import Literal, Union, List, Optional, TypeAlias
from enum import Enum

# import streamlit as st
from pydantic import BaseModel, Field, fields
# import streamlit_pydantic as sp

from pydantic.config import ConfigDict

class SmallMolecule(BaseModel):
    
    Name: str
    Duration: str
    Concentration: str

class CRISPR(BaseModel):
    
    Name: str
    Duration: str
    Concentration: str

class RNAi(BaseModel):
    
    Name: str
    Duration: str
    Concentration: str

class Antibody(BaseModel):
    
    Name: str
    Duration: str
    Concentration: str

class ProteinP(BaseModel):
    
    model_config = ConfigDict(title='Protein')

    Name: str
    Duration: str
    Concentration: str

class InfectiousAgent(BaseModel):
    
    Name: str
    Duration: str
    Concentration: str

class EpigeneticModification(BaseModel):
    
    Name: str

class Protein(BaseModel):
    
    Name: str

class Transcript(BaseModel):
    
    Name: str

class Gene(BaseModel):
    
    Name: str

class Tissue(BaseModel):
    
    Name: str

class PrimaryCells(BaseModel):
    
    Name: str

class DifferentiatedCells(BaseModel):
    
    Name: str

class iPSC(BaseModel):
    
    Name: str

class CellLine(BaseModel):
    
    Name: str

class Wastewater(BaseModel):
    
    Name: str

class PatientSample(BaseModel):
    
    Name: str

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
   
    type: Union[
            CellLine,
            iPSC,
            DifferentiatedCells,
            PrimaryCells,
            Tissue
            ]


class Sample(BaseModel):
    
    SampleName: str
    Description: str
    ExperimentalSubject: Union[
            ModelSystem,
            Biospecimen,
            Target
            ]
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