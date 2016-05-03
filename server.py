#!/usr/bin/env python3

import argparse
from bottle import abort, error, post, request, run
import json
from networkx.readwrite import json_graph

from conceptgraphs import Graph as CG
from conceptgraphs.transformers import transformer_dict

arg_parser = argparse.ArgumentParser(description='REST server for concept graphs')
arg_parser.add_argument('-H','--hostname',help='hostname to bind to',default='localhost')
arg_parser.add_argument('-P','--port',type=int,help='port number to bind to',default=9000)
arg_parser.add_argument('-t','--default-transformer',help='transformer to use by default',default='deep')
args = arg_parser.parse_args()


transformers = transformer_dict.copy()

def getTransformer (modules):
    name = '__'.join(modules)
    if name in transformers:
        return transformers[name]
    else:
        try:
            T = type(name, tuple(transformer_dict[m] for m in modules), {})
            transformers[name] = T
            return T
        except KeyError:
            abort(400,"Inexistent transformer name")

class SkipEncoder(json.JSONEncoder):
    def default(self, obj):
        return None

def postGraph (graph):
    g = graph._g
    for n in g:
        g.node[n]['label'] = g.node[n]['concept']
        for m in g[n]:
            g[n][m]['label'] = g[n][m]['functor']
    return json.dumps(json_graph.node_link_data(g), cls=SkipEncoder)

### ROUTES ###

@post('/')
def extract():
    req = request.json
    text = req.get('text')
    trans = req.get('transformers', args.default_transformer)
    try:
        trans = [t.strip() for t in trans.split(',')]
    except AttributeError:
        pass
    T = getTransformer(trans)
    graph = CG(transformer=T(),text=text)
    return postGraph(graph)

@error(400)
def custom400 (error):
    return json.dumps({
        'error': True,
        'message': error.body
        })

run(host=args.hostname,port=args.port)
