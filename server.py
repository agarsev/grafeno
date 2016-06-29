#!/usr/bin/env python3

# Grafeno -- Python concept graphs library
# Copyright 2016 Antonio F. G. Sevilla <afgs@ucm.es>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import argparse

import bottle
from bottle import static_file, abort, error, get, post, request, run, view
bottle.TEMPLATE_PATH = [ 'res' ]

import json
import re
import unicodedata
import yaml

from grafeno import pipeline

arrayize = lambda t: t.split(',')
arg_parser = argparse.ArgumentParser(description='REST server for concept graphs')
arg_parser.add_argument('-H','--hostname',help='hostname to bind to',default='localhost')
arg_parser.add_argument('-P','--port',type=int,help='port number to bind to',default=9000)
args = arg_parser.parse_args()

control_chars = ''.join([chr(x) for x in range(0,32)] + [chr(x) for x in range(127,160)])
control_char_re = re.compile('[%s]' % re.escape(control_chars))
def remove_control_chars(s):
    return control_char_re.sub(' ', s)

def run_pipeline (config):
    try:
        result = pipeline.run(config)
    except ValueError as e:
        abort(400,str(e))
    try:
        j = result.to_json()
        result = json.loads(j)
    except AttributeError:
        pass
    return json.dumps({
        'ok': True,
        'result': result
        })

# ROUTES

@post('/raw')
def raw_request():
    try:
        config = request.json
    except ValueError:
        abort(400,"Invalid json request")
    return run_pipeline(config)

@post('/run/<config_file>')
def stored_config(config_file):
    try:
        reqbody = request.json
    except ValueError:
        abort(400,"Invalid json request")
    try:
        config_file = open('configs/'+config_file+'.yaml')
    except FileNotFoundError:
        abort(400,"Unknown configuration "+config_file)
    config = yaml.load(config_file)
    config.update(reqbody)
    return run_pipeline(config)

@get('/run/<config_file>')
@view('config')
def view_config(config_file):
    try:
        cfile = open('configs/'+config_file+'.yaml')
    except FileNotFoundError:
        abort(404,"Unknown configuration "+config_file)
    try:
        text = open('default.txt').read()
    except FileNotFoundError:
        text = "John loves Mary."
    return dict(name=config_file, config=cfile.read(), default_text=text)

@error(400)
def custom400 (error):
    return json.dumps({
        'ok': False,
        'error_message': error.body
        })

@error(500)
def custom500 (error):
    return json.dumps({
        'ok': False,
        'error_message': error.body
        })


# OTHER THINGS

@get('/static/logo.svg')
def get_logo ():
    return static_file('logo.svg',root='res')

from nltk.corpus import wordnet as wn
@get('/other/synonyms/<word>')
def get_synonyms(word):
    '''For Alberto's alternative project'''
    if word is None:
        abort(400,"No word")
    synonyms = set(l.name() for ss in wn.synsets(word) for l in ss.lemmas())
    return json.dumps({'synonyms': list(synonyms)})

# RUN SERVER

run(host=args.hostname,port=args.port,reloader=True)
