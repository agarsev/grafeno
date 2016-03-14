#!/usr/bin/env python3

from collections import deque

import conceptgraphs.operations as cop
from conceptgraphs import Functor, Graph as CG

from nltk.corpus import wordnet as wn

def extend (cgraph):
    g = cgraph._g
    hypers = {}
    to_extend = deque(g.nodes())
    while len(to_extend)>0:
        n = to_extend.popleft()
        node = g.node[n]
        if 'hyper' in node['gram']:
            syn = wn.synset(node['concept'])
            if syn.min_depth()<10:
                continue
            ss = syn.hypernyms()
        else:
            pos = node['gram']['type']
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
            cgraph.add_edge(n, nu, Functor.HYP)


if __name__ == "__main__":

    import argparse, sys

    arg_parser = argparse.ArgumentParser(description='Summarize text via concept graphs')
    arg_parser.add_argument('text', nargs='*', help='Text file to summarize')
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    arg_parser.add_argument('-l','--linearize',help="Linearizing module to use",default='simple_nlg')
    args = arg_parser.parse_args()

    sys.path.insert(1, 'modules')

    if len(args.text)>0:
        text = ' '.join(args.text)
    else:
        text = sys.stdin.read()

    T = __import__(args.transform)
    cg = CG(grammar=T.grammar, text=text)
    extend(cg)
    for cl in cop.cluster(cg).clusters:
        cg.draw(cl)
