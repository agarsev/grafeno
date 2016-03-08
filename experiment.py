#!/usr/bin/env python3

from conceptgraphs import Graph as CG

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
    na = a._g.node[an]
    nb = b._g.node[bn]
    if na['gram']['type'] != nb['gram']['type']:
        return None
    com=get_common_concept(na, nb)
    if com == None:
        return None
    node = G.add_node(com, na['gram'])
    for i in a._g[an]:
        for j in b._g[bn]:
            if a._g[an][i]['functor'] == b._g[bn][j]['functor']:
                d = generalize_rec(G, a, b, i, j)
                if d != None:
                    G.add_edge(node, d, a._g[an][i]['functor'],
                            a._g[an][i]['gram'])
    return node

def generalize (a, b):
    gen = CG()
    generalize_rec(gen, a, b, 0, 0)
    return gen

def rave (cg, node=0):
    sss = wn.synsets(cg._g.node[node]['concept'])
    opts = [ss.closure(lambda s: s.hyponyms(), depth=2) for ss in sss]
    opts = sss + [s for o in opts for s in o]
    alt = random.choice(opts)
    cg._g.node[node]['concept'] = alt.lemma_names()[0]
    for n in cg._g[node]:
        rave(cg, n)


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
        gs = [reduce(generalize, gs)]

    if args.rave:
        for g in gs:
            rave(g)

    if args.print:
        for g in gs:
            g.draw()

    L = __import__(args.linearize)
    for g in gs:
        print(L.linearize(g._g))
