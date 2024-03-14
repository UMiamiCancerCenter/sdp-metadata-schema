
"""
Demonstration of dynamic model creation.

You could use this technique to load something from mongo or a file
"""


import json
# from enum import Enum
import random
from typing import Union

from typing_extensions import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from pydantic import create_model

import networkx as nx
from IPython import embed


def build_tree(node, G, forms):
    """recursively build the subtrees and add them to this tree."""
    children = [] 
    for child in G.neighbors(node):
        submodel = build_tree(child, G, forms)
        children.append(submodel)
    value = random.randint(128, 256)
    qualname =f"Model {node}" 
    if len(children) > 0:
        model = create_model(qualname,
                             children=(Union[tuple(children)], ...))
    else:
        args = forms.get(node)
        if args is None:
            print("key not found", args)
            args = {node:(str, ...)}
        else:
            print(node.center(80,"#"))
            withtypes = {}
            for k,v in args.items():
                if v == "str":
                    withtypes[k] = (str, ...)
                elif v == "int":
                    withtypes[k] = (int, ...)
            args = withtypes
        model = create_model(qualname, **args)
    setattr(model, "__qualname__", qualname)

    return model


def example():
    """ call this from main to see if the schema worked """
    tree = nx.generators.trees.random_tree(17, seed=17,
                                           create_using=nx.DiGraph())
    root = list(nx.topological_sort(tree))[0]
    tree_model = build_tree(root, tree, None)
    print(json.dumps(tree_model.model_json_schema(), indent=2))
