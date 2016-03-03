#!/usr/bin/env python3

from freeling_parse import parse
from extract_concepts import transform_tree
from common import draw_concept_graph

import networkx as nx

import nltk
from nltk.corpus import wordnet as wn

def get_common_concept(a, b):
    try:
        ssa = wn.synsets(a['concept'])
        ssb = wn.synsets(b['concept'])
        commons = [x for a in ssa for b in ssb for x in a.lowest_common_hypernyms(b) ]
        commons.sort(key=lambda x: x.max_depth(), reverse=True)
        return commons[0].lemma_names()[0]
    except IndexError:
        return None

def generalize_rec (G, a, b, an, bn):
    global n
    com=get_common_concept(a.node[an], b.node[an])
    if com == None:
        return None
    node = n
    n += 1
    G.add_node(node, concept=com)
    for i in a[an]:
        for j in b[bn]:
            if a[an][i]['type'] == b[bn][j]['type']:
                d = generalize_rec(G, a, b, i, j)
                G.add_edge(node, d, type=a[an][i]['type'])
    return node

def generalize (a, b):
    global n
    n = 0
    G = nx.DiGraph()
    generalize_rec(G, a, b, 0, 0)
    return G


if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Do an experiment')
    arg_parser.add_argument('s1', help='a sentence')
    arg_parser.add_argument('s2', help='another sentence')
    arg_parser.add_argument('-p', '--print', action='store_true', help='display the concept graphs')
    args = arg_parser.parse_args()

    gs = [transform_tree(parse(s)) for s in [args.s1, args.s2]]

    if args.print:
        for g in gs:
            draw_graph(g)

    draw_concept_graph(generalize(*gs))
