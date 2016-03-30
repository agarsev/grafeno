#!/usr/bin/env python3

import sys

from collections import deque

import conceptgraphs.operations as cop
from conceptgraphs import Functor, Graph as CG

from nltk.corpus import wordnet as wn

import nltk

def extend (cgraph, min_depth, weight):
    g = cgraph._g
    hypers = {}
    to_extend = deque(g.nodes())
    while len(to_extend)>0:
        n = to_extend.popleft()
        node = g.node[n]
        if 'hyper' in node['gram']:
            syn = wn.synset(node['concept'])
            if syn.min_depth()<min_depth:
                continue
            ss = syn.hypernyms()
        else:
            pos = node['gram']['sempos']
            if pos != 'N':
                continue
            ss = wn.synsets(node['concept'], pos.lower())
        for s in ss:
            name = s.name()
            if name in hypers:
                nu = hypers[name]
            else:
                nu = cgraph.add_node(s.name(), gram={'hyper':True})
                hypers[name] = nu
                to_extend.append(nu)
            cgraph.add_edge(n, nu, Functor.HYP, weight=weight)


sys.path.insert(1, 'modules')
Ext = __import__('tag_extract')

def concept_coverage (graph, text, tags):
    surf = CG(grammar=Ext.tag_extract(tags), text=text)
    surf_concepts = set(surf._g.node[n]['concept'] for n in surf._g.nodes())
    graph_concepts = set(graph._g.node[n]['concept'] for n in graph._g.nodes())
    return len(graph_concepts & surf_concepts)/len(surf_concepts)

if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Summarize text via concept graphs')
    arg_parser.add_argument('fulltext', help='Text file with the original text')
    arg_parser.add_argument('summary', help='Text file with a correct summary')
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    arg_parser.add_argument('-d','--depth',type=int,help="Minimum conceptual depth for hypernyms to use for extension",default=5)
    arg_parser.add_argument('-w','--weight',type=float,help="Weight to assign to hypernym relations",default=0.5)
    args = arg_parser.parse_args()

    with open(args.fulltext) as f:
        text = f.read()

    with open(args.summary) as f:
        summ = f.read()

    T = __import__(args.transform)

    cg = CG(grammar=T.grammar, text=text)
    extend(cg, args.depth, args.weight)
    clusters = cop.cluster(cg).clusters
    biggest = sorted(clusters, key=len, reverse=True)[0]
    filtered = [n for n in biggest if not 'hyper' in cg._g.node[n]['gram']]
    #cg.draw(filtered)

    sc = CG(grammar=T.grammar, text=summ)
    #sc.draw()
    print(concept_coverage(cg, summ, {'N','V','J'}))
    print(concept_coverage(sc, summ, {'N','V','J'}))
