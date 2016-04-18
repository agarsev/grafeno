#!/usr/bin/env python3

from collections import deque
from itertools import combinations
from nltk.corpus import wordnet as wn
import nltk.data
from subprocess import Popen, PIPE
import subprocess as subp
import re

from conceptgraphs import Graph as CG

simparse = re.compile('([0-9.]+)$')
def link_all (cgraph, nodes, threshold = 100, weight = 1):
    g = cgraph._g
    for n, m in combinations(nodes, 2):
        sa = g.node[n]['concept']
        sb = g.node[m]['concept']
        proc = Popen(["/usr/bin/env", "WNSEARCHDIR=/usr/share/wordnet", "similarity.pl", "--type", "WordNet::Similarity::lesk",\
                sa,sb], stdin=PIPE,stdout=PIPE,stderr=PIPE)
        data, err = proc.communicate()
        res = simparse.search(data.decode('UTF-8'))
        sim = int(res.group(0))
        if sim > threshold:
            cgraph.add_edge(n, m, 'SIM', {'weight':weight})
            cgraph.add_edge(m, n, 'SIM', {'weight':weight})

def vote (sentence, graph, HVS, clusters):
    g = graph._g
    extended = set()
    to_extend = deque(sentence)
    while len(to_extend)>0:
        n = to_extend.popleft()
        if n in extended:
            continue
        extended.add(n)
        for h in g[n]:
            if g[n][h]['functor'] == 'HYP':
                to_extend.append(h)
    scores = []
    for h, c in zip(HVS, clusters):
        score = 0
        for o in extended:
            if o in h:
                score += 1
            elif o in c:
                score += 0.5
        scores.append(score)
    return scores

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def get_full_sentences (text):
    return tokenizer.tokenize(text, realign_boundaries=True)

if __name__ == "__main__":

    import argparse, sys, importlib

    arg_parser = argparse.ArgumentParser(description='Replicate Plaza summary by extraction method')

    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')
    arg_parser.add_argument('--similarity-links',action='store_true',help='Use extra similarity links (takes a *lot* of time)')
    arg_parser.add_argument('--thesis-clustering',action='store_true',help='Do clustering as in the thesis')
    arg_parser.add_argument('--hubratio',type=float,default=0.2,help='Percentage of hub vertices (from 0 to 1)')
    arg_parser.add_argument('-t','--transformer',default='plaza',help='Transformer module to use')

    args = arg_parser.parse_args()

    text = args.fulltext.read()
    full = get_full_sentences(text)

    trmod = importlib.import_module('modules.'+args.transformer)
    tr = trmod.Transformer()
    graph = CG(transformer=tr, text=text)

    if args.similarity_links:
        link_all(graph, [n for s in tr.sentences for n in s])

    if args.thesis_clustering:
        from conceptgraphs.thesis import cluster
    else:
        from conceptgraphs.clustering import cluster
    HVS, clusters = cluster(graph, args.hubratio)

    # Heuristica 1
    best_cluster = max(range(len(clusters)), key=lambda i: len(clusters[i]))

    sentence_scores = []
    for s in tr.sentences:
        cluster_scores = vote(s, graph, HVS, clusters)
        sentence_scores.append(cluster_scores[best_cluster])

    best = sorted(range(len(sentence_scores)), reverse=True, key=lambda i:sentence_scores[i])
    print('\n'.join(s for i, s in enumerate(full) if i in best[:5]))
