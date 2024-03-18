
"""
Demonstration of dynamic model creation.

You could use this technique to load something from mongo or a file
"""


import json
# from enum import Enum
from typing import Union

from typing_extensions import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from pydantic import create_model


class FooBar(BaseModel):
    """A static class to incorporate dynamically."""
    count: int
    size: Union[float, None] = None


class StaticModel(BaseModel):
    """
    This is the description of the main model
    """

    model_config = ConfigDict(title='Static')

    foo_bar: Annotated[FooBar, Field(widget='checkbox')]
    form_type: bool = Field(
        False,
        title='boolean',
        description='a boolean field',
    )


def example():
    """ call this from main to see if the schema worked """
    Dyn_model = create_model("Dynamic",
                             source=(str, "dynamic"), type=(int, 15),
                             gt=(int, 11), lt=(int, 20),
                             static=(StaticModel, ...))
    print(json.dumps(Dyn_model.model_json_schema(), indent=2))
