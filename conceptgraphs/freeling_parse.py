#!/usr/bin/env python3

from subprocess import Popen, PIPE
import subprocess as subp
import json
import re

regex = re.compile('}\s*{')

def parse (sentence, semgraph=False):
    if semgraph:
        config = "conceptgraphs/freeling_full.cfg"
    else:
        config = "conceptgraphs/freeling_deps.cfg"
    proc = Popen(["analyze", "--flush", "-f", config], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data, err = proc.communicate(sentence.encode('UTF-8'))
    if semgraph:
        return json.loads(data.decode('UTF-8'))
    else:
        return json.loads('['+regex.sub('},{',data.decode('UTF-8'))+']')

def get_functor (name):
    if name.startswith('A0'):
        return 'AGENT'
    if name.startswith('A1'):
        return 'THEME'
    if name.startswith('AM'):
        return 'ATTR'
    return '?.'+name

def extract_semgraph (parse, graph):
    sg = parse['semantic_graph']

    ents = {}

    for e in sg['entities']:
        concept = e['lemma'].partition('.')[0]
        nid = graph.add_node(concept=concept,gram={'sempos':'n'})
        ents[e['id']] = nid

    for f in sg['frames']:
        concept = f['lemma'].partition('.')[0]
        nid = graph.add_node(concept=concept,gram={'sempos':'v'})
        ents[f['id']] = nid

    for f in sg['frames']:
        for a in f['arguments']:
            head, child = f['id'], a['entity']
            if head not in ents or child not in ents:
                continue
            graph.add_edge(ents[head], ents[child], \
                    functor=get_functor(a['role']), gram={})

