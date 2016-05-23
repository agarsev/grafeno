#!/usr/bin/env python3

import argparse
from collections import deque

from conceptgraphs import Graph as CG, transformers
from conceptgraphs.thesis import cluster

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

DEFAULT_PIPELINE = ['pos_extract', 'sentences', 'unique', 'extend', 'sim_link']

arg_parser = argparse.ArgumentParser(description='Replicate Plaza summary by extraction method')

arrayize = lambda t: t.split(',')
arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')
arg_parser.add_argument('--hubratio',type=float,default=0.2,help='Percentage of hub vertices (from 0 to 1)')
arg_parser.add_argument('-t','--transformers',type=arrayize,help='transformer pipeline to use',default=DEFAULT_PIPELINE)
arg_parser.add_argument('--length',type=int,default=100,help='Approximate number of words for the summary to have')
arg_parser.add_argument('--margin',type=int,default=10,help='Upper margin for the length of the summary')

args = arg_parser.parse_args()

text = args.fulltext.read()

graph = CG(transformer=transformers.get_pipeline(args.transformers), text=text)

HVS, clusters = cluster(graph, args.hubratio)

# Heuristica 1
best_cluster = max(range(len(clusters)), key=lambda i: len(clusters[i]))

sentence_scores = []
for s in graph.gram['sentence_nodes']:
    cluster_scores = vote(s, graph, HVS, clusters)
    sentence_scores.append(cluster_scores[best_cluster])

best = sorted(range(len(sentence_scores)), reverse=True, key=lambda i:sentence_scores[i])
length = 0
last = 0
full = graph.gram['sentences']
while length < args.length and last<len(best):
    length += len(full[best[last]].split(' '))
    if length < args.length + args.margin:
        last += 1
print('\n'.join(s for i, s in enumerate(full) if i in best[:last]))
