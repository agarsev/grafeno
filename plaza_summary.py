#!/usr/bin/env python3

from itertools import combinations
from nltk.corpus import wordnet as wn
from subprocess import Popen, PIPE
import subprocess as subp
import re

from conceptgraphs import Graph as CG
import conceptgraphs.operations as cop

from modules.plaza import Grammar

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

if __name__ == "__main__":

    import argparse, sys, importlib

    arg_parser = argparse.ArgumentParser(description='Replicate Plaza summaryzation method')

    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')

    args = arg_parser.parse_args()

    text = args.fulltext.read()
    parser = Grammar()
    graph = CG(grammar=parser, text=text)

    link_all(graph, [n for s in parser.sentences for n in s])
    graph.draw()
    #clusters = cop.cluster(graph).clusters
    #clusters = sorted(clusters, key=len, reverse=True)
    #for c in clusters:
        #graph.draw(c)

