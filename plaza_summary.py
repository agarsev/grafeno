#!/usr/bin/env python3

from itertools import combinations
from nltk.corpus import wordnet as wn

from conceptgraphs import Graph as CG
import conceptgraphs.operations as cop

from modules.plaza import Grammar

def get_semantic_similarity (x, xpos, y, ypos):
    # TODO: Usar lesk
    r = 0
    for sx in wn.synsets(x, 'n'):
        for sy in wn.synsets(y, 'n'):
            sim = sx.lch_similarity(sy)
            if sim and sim>r:
                r = sim
    return r

def link_all (cgraph, threshold = 1, weight = 1):
    g = cgraph._g
    for n, m in combinations(g.nodes(), 2):
        nn = g.node[n]
        nm = g.node[m]
        sim = get_semantic_similarity(nn['concept'], nn['gram']['sempos'], nm['concept'], nm['gram']['sempos'])
        if sim > threshold:
            cgraph.add_edge(n, m, 'SIM', {'weight':weight})
            cgraph.add_edge(m, n, 'SIM', {'weight':weight})

if __name__ == "__main__":

    import argparse, sys, importlib

    arg_parser = argparse.ArgumentParser(description='Replicate Plaza summaryzation method')

    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')

    args = arg_parser.parse_args()

    text = args.fulltext.read()
    graph = CG(grammar=Grammar(), text=text)
    link_all(graph)
    graph.draw()
    #clusters = cop.cluster(graph).clusters
    #clusters = sorted(clusters, key=len, reverse=True)
    #for c in clusters:
        #graph.draw(c)

