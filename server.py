#!/usr/bin/env python3

import argparse
from bottle import abort, error, get, post, request, run
import re
import unicodedata

from conceptgraphs import Graph as CG, transformers, linearizers

arg_parser = argparse.ArgumentParser(description='REST server for concept graphs')
arg_parser.add_argument('-H','--hostname',help='hostname to bind to',default='localhost')
arg_parser.add_argument('-P','--port',type=int,help='port number to bind to',default=9000)
arg_parser.add_argument('-t','--default-transformer',help='transformer to use by default',default=['semantic'])
arg_parser.add_argument('-l','--default-linearizer',help='linearizer to use by default',default=['simple_nlg'])
arg_parser.add_argument('-o','--default-operations',action='append',help='operation pipeline to run by default',default=['extract','linearize'])

args = arg_parser.parse_args()

control_chars = ''.join([chr(x) for x in range(0,32)] + [chr(x) for x in range(127,160)])
control_char_re = re.compile('[%s]' % re.escape(control_chars))
def remove_control_chars(s):
    return control_char_re.sub(' ', s)

from nltk.corpus import wordnet as wn
import json
@get('/synonyms/<word>')
def get_synonyms(word):
    '''For Alberto's alternative project'''
    if word is None:
        abort(400,"No word")
    synonyms = set(l.name() for ss in wn.synsets(word) for l in ss.lemmas())
    return json.dumps({'synonyms': list(synonyms)})

memory = {}
# Request:
#  'name': name of concept graph in server
#  'operations': [ str ]
#      'extract': <text, transformers> create a graph from the text
#      'linearize': <linearizers> return text from graph
#      'to_json': return full graph as json
#  'text': str
#  'transformers': [ str ]
#  'transformer_args': dict
#  'linearizers': [ str ]
#  'linearizer_args': dict
# -->
#  'result': json | text
@post('/')
def main():
    global memory
    try:
        req = request.json
    except ValueError:
        abort(400,"Invalid json request")
    name = req.get('name')
    graph = memory.get(name) if name else None
    text = remove_control_chars(req.get('text'))
    ret = dict()
    for op in req.get('operations',args.default_operations):
        if op == 'extract':
            try:
                text = req['text']
            except KeyError:
                abort(400,"Required parameter missing: text")
            try:
                T = transformers.get_pipeline(req.get('transformers', args.default_transformer))
            except KeyError:
                abort(400,"Unknown transformer pipeline")
            graph = CG(transformer=T,transformer_args=req.get('transformer_args',{}),text=text)
        elif op == 'linearize':
            try:
                L = linearizers.get_pipeline(req.get('linearizers', args.default_linearizer))
            except KeyError:
                abort(400,"Unknown linearizer pipeline")
            ret['result'] = graph.linearize(linearizer=L,linearizer_args=req.get('linearizer_args',{}))
        elif op == 'to_json':
            ret['result'] = json.loads(graph.to_json())
    if name:
        memory[name] = graph
    return json.dumps(ret)

@error(400)
def custom400 (error):
    return json.dumps({
        'error': True,
        'error_message': error.body
        })

@error(500)
def custom500 (error):
    return json.dumps({
        'error': True,
        'error_message': error.body
        })

run(host=args.hostname,port=args.port)
