
""" an example with branching choices """

import json
from typing import Literal, Union
from enum import Enum

from pydantic import BaseModel, Field

from pydantic.config import ConfigDict

class EpigeneticModification(BaseModel):
    
    SampleName: str

class Protein(BaseModel):
    
    SampleName: str

class Transcript(BaseModel):
    
    SampleName: str

class Gene(BaseModel):
    
    SampleName: str

class Tissue(BaseModel):
    
    SampleName: str

class PrimaryCells(BaseModel):
    
    SampleName: str

class DifferentiatedCells(BaseModel):
    
    SampleName: str

class iPSC(BaseModel):
    
    SampleName: str

class CellLine(BaseModel):
    
    SampleName: str

class Wastewater(BaseModel):
    
    SampleName: str

class PatientSample(BaseModel):
    
    SampleName: str

class Target(BaseModel):
    """ not sure how to get numbering on the others. Not important"""
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


class ExperimentalSubject(BaseModel):
    """ Dialog can have one role"""

    role: Union[
            ModelSystem,
            Biospecimen,
            Target
            ] 


def example():
    """ run this to see the schema dumped """
    with open ("genmeta_schema.json", "w") as ft:
        print(json.dumps(ExperimentalSubject.model_json_schema(), indent=2), 
              file = ft)

example()