
""" an example with branching choices """

import json
from typing import Literal, Union
from enum import Enum

from pydantic import BaseModel, Field

from pydantic.config import ConfigDict


class English(BaseModel):
    """ will have three required fields """
    language: Literal["en"]
    one: int
    two: int
    three: int


class GermanCount(int, Enum):
    """ not sure how to get numbering on the others. Not important"""
    EINS = 1
    ZWEI = 2
    DREI = 3


class German(BaseModel):
    """ will have one field, with three options"""
    language: Literal["de"]
    model_config = ConfigDict(arbitrary_types_allowed=True)
    numbers: Union[GermanCount.EINS,
                   GermanCount.ZWEI,
                   GermanCount.DREI
                   ]


class Japanese(BaseModel):
    """ will have four fields """
    language: Literal["jp"]
    ichi: int
    ni: int
    san: int
    shi: int


class Dialog(BaseModel):
    """ Dialog can have one language"""

    language: Union[
            English,
            German,
            Japanese] = Field(discriminator="language")


def example():
    """ run this to see the schema dumped """
    print(json.dumps(Dialog.model_json_schema(), indent=2))
