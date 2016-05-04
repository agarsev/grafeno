#!/usr/bin/env python3

import argparse
from bottle import abort, error, post, request, run

from conceptgraphs import Graph as CG
from conceptgraphs.transformers import get_pipeline

arg_parser = argparse.ArgumentParser(description='REST server for concept graphs')
arg_parser.add_argument('-H','--hostname',help='hostname to bind to',default='localhost')
arg_parser.add_argument('-P','--port',type=int,help='port number to bind to',default=9000)
arg_parser.add_argument('-t','--default-transformer',help='transformer to use by default',default='deep')
args = arg_parser.parse_args()

@post('/')
def extract():
    req = request.json
    text = req.get('text')
    trans = req.get('transformers', args.default_transformer)
    try:
        trans = [t.strip() for t in trans.split(',')]
    except AttributeError:
        pass
    try:
        T = get_pipeline(trans)
    except KeyError:
        abort(400,"Invalid transformers")
    graph = CG(transformer=T,transformer_args=req.get('args',{}),text=text)
    return graph.to_json()

@error(400)
def custom400 (error):
    return json.dumps({
        'error': True,
        'message': error.body
        })

run(host=args.hostname,port=args.port)
