#!/usr/bin/env python3

import conceptgraphs.graph as CG

import networkx as nx

import nltk
from nltk.corpus import wordnet as wn

import random
from functools import reduce

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
    na = a.node[an]
    nb = b.node[bn]
    if na['type'] != nb['type']:
        return None
    com=get_common_concept(na, nb)
    if com == None:
        return None
    node = n
    n += 1
    G.add_node(node, concept=com, type=na['type'])
    for i in a[an]:
        for j in b[bn]:
            if a[an][i]['type'] == b[bn][j]['type']:
                d = generalize_rec(G, a, b, i, j)
                if d != None:
                    G.add_edge(node, d, type=a[an][i]['type'])
    return node

def generalize (a, b):
    global n
    n = 0
    G = nx.DiGraph()
    generalize_rec(G, a, b, 0, 0)
    return G

def rave (g, node=0):
    sss = wn.synsets(g.node[node]['concept'])
    opts = [ss.closure(lambda s: s.hyponyms(), depth=2) for ss in sss]
    opts = sss + [s for o in opts for s in o]
    alt = random.choice(opts)
    g.node[node]['concept'] = alt.lemma_names()[0]
    for n in g[node]:
        rave (g, n)


if __name__ == "__main__":

    import argparse, sys

    arg_parser = argparse.ArgumentParser(description='Do an experiment')
    arg_parser.add_argument('sent', nargs='+', help='one or more sentences')
    arg_parser.add_argument('-p', '--print', action='store_true', help='display the concept graph for the generalization')
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    arg_parser.add_argument('-l','--linearize',help="Linearizing module to use",default='simple_nlg')
    arg_parser.add_argument('-g','--generalize',action="store_true",help="Generalize two sentences")
    arg_parser.add_argument('-r','--rave',action="store_true",help="Distort the concept graph by raving")
    args = arg_parser.parse_args()

    sys.path.insert(1, 'modules')

    T = __import__(args.transform)
    gs = [CG(T.rules, text=s) for s in args.sent]

    if args.generalize:
        nu = CG(T.rules)
        nu.g = reduce(generalize, [g.g for g in gs])
        gs = [nu]

    if args.rave:
        for g in gs:
            rave(g.g)

    if args.print:
        for g in gs:
            g.draw()

    L = __import__(args.linearize)
    for g in gs:
        print(L.linearize(g.g))
