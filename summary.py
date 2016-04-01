#!/usr/bin/env python3

from collections import deque, namedtuple
import math

import nltk
from nltk.corpus import wordnet as wn

from conceptgraphs import Functor, Graph as CG
import conceptgraphs.operations as cop

from modules.tag_extract import tag_extract


Metrics = namedtuple('Metrics', ['precision', 'recall', 'f'])


def concept_coverage (graph, text, tags={'N','V','J','R'}):
    text_concepts = CG(grammar=tag_extract(tags), text=text).all_concepts()
    graph_concepts = graph.all_concepts()

    overlap = len(graph_concepts & text_concepts)
    prec = overlap / len(graph_concepts)
    recall = overlap / len(text_concepts)
    f = 2*recall*prec/(recall+prec)
    return Metrics(prec,recall,f)


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
            cgraph.add_edge(n, nu, Functor.HYP, {'weight':weight})

hit_functions = {
    'auth': lambda auth, hub: auth,
    'hub': lambda auth, hub: hub,
    'sum': lambda auth, hub: auth+hub,
    'norm': lambda auth, hub: math.sqrt(auth**2+hub**2)
}

if __name__ == "__main__":

    import argparse, sys

    arg_parser = argparse.ArgumentParser(description='Summarize a text and evaluate the resultant summary against a good one')

    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')
    arg_parser.add_argument('summary', type=argparse.FileType('r'), help='Text file with a good summary')

    arg_parser.add_argument('--baseline',action='store_true',help="Baseline experiment: take the first appearing concepts in the text")
    arg_parser.add_argument('--clustering',action='store_true',help="Clustering experiment: take the biggest cluster in the conceptual graph")
    arg_parser.add_argument('--hits',action='store_true',help="HITS experiment: take the nodes with higher AUTH")
    arg_parser.add_argument('--all',action='store_true',help="Run all experiments")

    arg_parser.add_argument('-r','--ratio', type=float, help='Compression rate to use for the summary', default=0.2)
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    arg_parser.add_argument('-d','--depth', type=int, help="Minimum conceptual depth for hypernyms to use for extension", default=5)
    arg_parser.add_argument('-w','--weight', type=float, help="Weight to assign to hypernym relations", default=0.5)
    arg_parser.add_argument('-v','--verbose', action='store_true', help='Show selected concepts for the summary')
    arg_parser.add_argument('-s','--show', action='store_true', help='Show the summary graph on-screen')
    arg_parser.add_argument('--sel-function', choices=hit_functions.keys(), help='Function to use to select the best nodes in HITS', default='hub')

    args = arg_parser.parse_args()

    if args.all:
        args.baseline = True
        args.clustering = True
        args.hits = True

    text = args.fulltext.read()
    summ = args.summary.read()

    graph = None

    def result (name, best_function):
        summary = graph.copy(best_function)
        if args.verbose:
            print(summary.all_concepts())
        if args.show:
            summary.draw()
        print(name+": "+str(concept_coverage(summary, summ)))

    if args.baseline or args.hits:
        graph = CG(grammar=tag_extract({'N','V','J','R'}), text=text)
        summary_length = int(len(graph._g.nodes())*args.ratio)

    if args.baseline:
        result('Baseline', lambda n: n['id']<summary_length)

    if args.clustering or args.hits:
        sys.path.insert(1, 'modules')
        T = __import__(args.transform)
        graph = CG(grammar=T.grammar, text=text)

    if args.clustering:
        ext = graph.copy()
        extend(ext, args.depth, args.weight)
        clusters = cop.cluster(ext).clusters
        biggest = sorted(clusters, key=len, reverse=True)[0]
        result('Clustering', lambda n: n['id'] in biggest)

    if args.hits:
        auth, hub = cop.hits(graph)
        best = sorted(graph._g.nodes(), key=lambda n: hit_functions[args.sel_function](auth[n], hub[n]), reverse=True)
        result('HITS', lambda n: n['id'] in best[:summary_length])

