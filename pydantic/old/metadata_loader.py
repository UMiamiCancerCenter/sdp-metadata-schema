import json

import yaml
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout


from randtree import build_tree

def main():
    with open ("metadata-v0.2.yaml") as fd:
        struct = yaml.safe_load(fd.read())
        print(struct) 
        graph = struct["graph"]
        forms = struct["forms"]
        G = nx.DiGraph(graph)
        print(G)
        root = list(nx.topological_sort(G))[0]
        tree_model = build_tree(root, G, forms)
        with open ("metadata_graph_model.json", "w") as ft:
            print(json.dumps(tree_model.model_json_schema(), indent=2), 
                  file = ft)
        # pos = nx.spring_layout(G)
        # pos = nx.nx_agraph.graphviz_layout(G, prog="dot", args="")
        pos = graphviz_layout(G, prog="dot")

        nx.draw_networkx(G, pos, font_size=6)    
        plt.savefig('genmeta-v0_2.png')

if __name__ == "__main__":
    main()
