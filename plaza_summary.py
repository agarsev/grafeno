#!/usr/bin/env python3

from collections import deque
from itertools import combinations
import nltk.data

from conceptgraphs import Graph as CG

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
    arg_parser.add_argument('--alternative-clustering',action='store_true',help='Do clustering as in the preliminary code')
    arg_parser.add_argument('--hubratio',type=float,default=0.2,help='Percentage of hub vertices (from 0 to 1)')
    arg_parser.add_argument('-t','--transformer',default='experiments.plaza',help='Transformer module to use')

    args = arg_parser.parse_args()

    text = args.fulltext.read()
    full = get_full_sentences(text)

    trmod = importlib.import_module(args.transformer)
    tr = trmod.Transformer()
    graph = CG(transformer=tr, text=text)

    if args.alternative_clustering:
        from conceptgraphs.clustering import cluster
    else:
        from conceptgraphs.thesis import cluster
    HVS, clusters = cluster(graph, args.hubratio)

    # Heuristica 1
    best_cluster = max(range(len(clusters)), key=lambda i: len(clusters[i]))

    sentence_scores = []
    for s in tr.sentences:
        cluster_scores = vote(s, graph, HVS, clusters)
        sentence_scores.append(cluster_scores[best_cluster])

    best = sorted(range(len(sentence_scores)), reverse=True, key=lambda i:sentence_scores[i])
    print('\n'.join(s for i, s in enumerate(full) if i in best[:5]))
