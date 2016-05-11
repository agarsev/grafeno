#!/usr/bin/env python3

import argparse
from bottle import abort, error, get, post, request, run
import re
import unicodedata

from conceptgraphs import Graph as CG
from conceptgraphs.transformers import get_pipeline as get_transformers

arg_parser = argparse.ArgumentParser(description='REST server for concept graphs')
arg_parser.add_argument('-H','--hostname',help='hostname to bind to',default='localhost')
arg_parser.add_argument('-P','--port',type=int,help='port number to bind to',default=9000)
arg_parser.add_argument('-t','--default-transformer',help='transformer to use by default',default='deep')
args = arg_parser.parse_args()

#all_chars = (unichr(i) for i in xrange(0x110000))
#control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
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

@post('/')
def extract():
    req = request.json
    text = remove_control_chars(req.get('text'))
    trans = req.get('transformers', args.default_transformer)
    try:
        trans = [t.strip() for t in trans.split(',')]
    except AttributeError:
        pass
    try:
        T = get_transformers(trans)
    except KeyError:
        abort(400,"Invalid transformers")
    graph = CG(transformer=T,transformer_args=req.get('args',{}),text=text)
    return graph.to_json()

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
