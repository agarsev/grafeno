#!/usr/bin/env python3

from freeling_parse import parse
from extract_concepts import transform_tree
import networkx as nx

if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Do an experiment')
    arg_parser.add_argument('s1', help='a sentence')
    args = arg_parser.parse_args()

    g = transform_tree(parse(args.s1))

    import matplotlib.pyplot as plt
    lay = nx.spring_layout(g)
    nx.draw_networkx(g,lay,node_size=1000,node_color="white", labels={n:data['concept'] for n, data in g.nodes(True)})
    nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['type'] for (a,b,data) in g.edges(data=True)})
    plt.show()
