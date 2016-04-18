#!/usr/bin/env python3

from conceptgraphs import Graph as CG
from conceptgraphs.operations import generalize

import nltk
from nltk.corpus import wordnet as wn

import random
from functools import reduce

def wordnet_common_concept(a, b):
    if a['gram']['sempos'] != b['gram']['sempos']:
        return None
    try:
        ssa = wn.synsets(a['concept'])
        ssb = wn.synsets(b['concept'])
        commons = [x for a in ssa for b in ssb for x in a.lowest_common_hypernyms(b) ]
        commons.sort(key=lambda x: x.max_depth(), reverse=True)
        gram = dict(a['gram'])
        gram['num'] = 'p'
        return { 'concept': commons[0].lemma_names()[0],
                 'gram': gram }
    except IndexError:
        return None

def rave (cg, node=0):
    sss = wn.synsets(cg._g.node[node]['concept'])
    opts = [ss.closure(lambda s: s.hyponyms(), depth=2) for ss in sss]
    opts = sss + [s for o in opts for s in o]
    alt = random.choice(opts)
    cg._g.node[node]['concept'] = alt.lemma_names()[0]
    for n in cg._g[node]:
        rave(cg, n)


if __name__ == "__main__":

    import argparse, sys, importlib

    arg_parser = argparse.ArgumentParser(description='Do an experiment')
    arg_parser.add_argument('sent', nargs='+', help='one or more sentences')
    arg_parser.add_argument('-p', '--print', action='store_true', help='display the concept graph for the generalization')
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='modules.deep_grammar')
    arg_parser.add_argument('-l','--linearize',help="Linearizing module to use",default='modules.simple_nlg')
    arg_parser.add_argument('-g','--generalize',action="store_true",help="Generalize two sentences")
    arg_parser.add_argument('-r','--rave',action="store_true",help="Distort the concept graph by raving")
    args = arg_parser.parse_args()

    T = importlib.import_module(args.transform)
    gs = [CG(T.Transformer(), text=s) for s in args.sent]

    if args.generalize:
        gs = [reduce(lambda a, b:
                generalize(a, b, node_generalize=wordnet_common_concept),
                gs)]

    if args.rave:
        for g in gs:
            rave(g)

    if args.print:
        for g in gs:
            g.draw()

    L = importlib.import_module(args.linearize)
    for g in gs:
        print(L.linearize(g))
