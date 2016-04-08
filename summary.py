#!/usr/bin/env python3

from collections import deque, namedtuple
from itertools import combinations
import math

import nltk
from nltk.corpus import wordnet as wn

from conceptgraphs import Graph as CG
import conceptgraphs.operations as cop

from modules.tag_extract import tag_extract


Metrics = namedtuple('Metrics', ['precision', 'recall', 'f'])


def concept_coverage (graph, text, tags={'N','V','J','R'}):
    text_concepts = CG(grammar=tag_extract(tags), text=text).all_concepts()
    graph_concepts = graph.all_concepts()

    overlap = len(graph_concepts & text_concepts)
    prec = overlap / len(graph_concepts)
    recall = overlap / len(text_concepts)
    f = 2*recall*prec/(recall+prec) if recall+prec > 0 else 0
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
            ss = syn.hypernyms() + syn.instance_hypernyms()
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
            cgraph.add_edge(n, nu, 'HYP', {'weight':weight})

def get_semantic_similarity (x, xpos, y, ypos):
    if xpos != ypos or xpos not in {'N','V'}:
        return 0
    r = 0
    for sx in wn.synsets(x, xpos.lower()):
        for sy in wn.synsets(y, ypos.lower()):
            sim = sx.lch_similarity(sy)
            if sim and sim>r:
                r = sim
    return r

def link_all (cgraph, threshold = 0.5, weight = 1):
    g = cgraph._g
    for n, m in combinations(g.nodes(), 2):
        nn = g.node[n]
        nm = g.node[m]
        sim = get_semantic_similarity(nn['concept'], nn['gram']['sempos'], nm['concept'], nm['gram']['sempos'])
        if sim > threshold:
            cgraph.add_edge(n, m, 'SIM', {'weight':weight})
            cgraph.add_edge(m, n, 'SIM', {'weight':weight})


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

    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('-r','--ratio', type=float, help='Compression rate to use for the summary', default=0.2)
    group.add_argument('-n','--number-of-words', type=int, help='Number of words to use for the summary')

    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    arg_parser.add_argument('-d','--depth', type=int, help="Minimum conceptual depth for hypernyms to use for extension", default=5)
    arg_parser.add_argument('-w','--weight', type=float, help="Weight to assign to hypernym relations", default=0.5)
    arg_parser.add_argument('-k','--keep-args', action='store_true', help='Keep arguments to verbs selected for the summary')
    arg_parser.add_argument('-l','--linearize', action='store_true', help='Linearize the summary graph')
    arg_parser.add_argument('-s','--show', action='store_true', help='Show the summary graph on-screen')
    arg_parser.add_argument('-q','--quiet', action='store_true', help='Print only the metrics without the description')
    arg_parser.add_argument('--sel-function', choices=hit_functions.keys(), help='Function to use to select the best nodes in HITS', default='hub')
    arg_parser.add_argument('--extend-for-hits', action='store_true', help='Extend graph when using HITS too')
    arg_parser.add_argument('--similarity-links', action='store_true', help='Link concepts in the graph with similarity links')

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
        met = concept_coverage(summary, summ)
        if args.quiet:
            print(' '.join(str(m) for m in met))
        else:
            print(name+": "+str(met))
        if args.linearize:
            from modules.simple_nlg import linearize
            print(linearize(summary))
        if args.show:
            summary.draw()

    graph = CG(grammar=tag_extract({'N','V','J','R'}), text=text)
    if args.number_of_words:
        summary_length = args.number_of_words
    else:
        summary_length = int(len(graph._g.nodes())*args.ratio)

    if args.baseline:
        result('Baseline', lambda n: n['id']<summary_length)

    if args.clustering or args.hits:
        sys.path.insert(1, 'modules')
        T = __import__(args.transform)
        graph = CG(grammar=T.grammar, text=text)
        if args.similarity_links:
            link_all(graph)

    if args.clustering or args.extend_for_hits:
        ext = graph.copy()
        extend(ext, args.depth, args.weight)

    if args.clustering:
        clusters = cop.cluster(ext).clusters
        clusters = sorted(clusters, key=len, reverse=True)
        summary, i, j = set(), 0, 0
        while len(summary) < summary_length:
            if j>=len(clusters[i]):
                j = 0
                i += 1
                if i>=len(clusters):
                    break
            nx = clusters[i][j]
            if nx in graph._g.nodes():
                summary.add(nx)
            j+=1
        result('Clustering', lambda n: n['id'] in summary)

    if args.hits:
        if args.extend_for_hits:
            auth, hub = cop.hits(ext)
        else:
            auth, hub = cop.hits(graph)
        best = sorted(graph._g.nodes(), key=lambda n: hit_functions[args.sel_function](auth[n], hub[n]), reverse=True)
        summary = set()
        i = 0
        while len(summary) < summary_length and i<len(best):
            nx = best[i]
            i += 1
            summary.add(nx)
            if args.keep_args:
                g = graph._g
                if g.node[nx]['gram']['sempos'] == 'V':
                    for m in g[nx]:
                        if g[nx][m]['functor'] in ('AGENT', 'THEME'):
                            summary.add(m)
        result('HITS', lambda n: n['id'] in summary)

