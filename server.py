#!/usr/bin/env python3

from bottle import post, run, request
import json
from networkx.readwrite import json_graph

from conceptgraphs import Graph as CG

from conceptgraphs.transformers.deep_grammar import Transformer as Deep
from conceptgraphs.transformers.sentence_record import Transformer as SentRecord
from conceptgraphs.transformers.extend import Transformer as Extend
from conceptgraphs.transformers.similarity_link import Transformer as SimLink


transformer = None


class Transformer (SimLink, Extend, Deep, SentRecord):
    pass


class SkipEncoder(json.JSONEncoder):

    def default(self, obj):
        return None


@post('/extract')
def extract():
    text = request.json.get('text')
    graph = CG(transformer=transformer,text=text)
    g = graph._g
    for n in g:
        g.node[n]['label'] = g.node[n]['concept']
        for m in g[n]:
            g[n][m]['label'] = g[n][m]['functor']
    return json.dumps(json_graph.node_link_data(g), cls=SkipEncoder)


if __name__ == "__main__":

    import argparse, sys, importlib

    arg_parser = argparse.ArgumentParser(description='REST server for concept graphs')

    arg_parser.add_argument('-H','--hostname',help='hostname to bind to',default='localhost')
    arg_parser.add_argument('-P','--port',type=int,help='port number to bind to',default=9000)

    args = arg_parser.parse_args()

    transformer = Transformer()

    run(host=args.hostname,port=args.port)
