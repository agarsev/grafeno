#!/usr/bin/env python3

import argparse
import yaml

from conceptgraphs import Graph as CG, transformers, linearizers

DEF_TRANSFORMERS = ['semantic']
DEF_T_ARGS = {}
DEF_LINEARIZERS = []
DEF_L_ARGS = {}

arrayize = lambda t: t.split(',')

arg_parser = argparse.ArgumentParser(description='Test script')
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-s','--string')
group.add_argument('-f','--file',type=argparse.FileType('r'))
arg_parser.add_argument('-t','--transformers',type=arrayize,help='transformer pipeline to use',default=DEF_TRANSFORMERS)
arg_parser.add_argument('-l','--linearizers',type=arrayize,help='linearizing pipeline to use',default=DEF_LINEARIZERS)
arg_parser.add_argument('-c','--config-file',type=argparse.FileType('r'),help='use a config file for pipeline options')
arg_parser.add_argument('-d','--display',action='store_true',help='display a drawing of the graph')
arg_parser.add_argument('-p','--print-json',action='store_true',help='print the graph in json')
args = arg_parser.parse_args()

if args.file:
    text = args.file.read()
else:
    text = args.string

if args.config_file:
    config = yaml.load(args.config_file)
    T = transformers.get_pipeline(config.get('transformers', DEF_TRANSFORMERS))
    T_args = config.get('transformer_args', DEF_T_ARGS)
    ls = config.get('linearizers', DEF_LINEARIZERS)
    L = linearizers.get_pipeline(ls) if len(ls)>0 else None
    L_args = config.get('linearizer_args', DEF_L_ARGS)
else:
    T = transformers.get_pipeline(args.transformers)
    T_args = DEF_T_ARGS
    L = linearizers.get_pipeline(args.linearizers) if len(args.linearizers)>0 else None
    L_args = DEF_L_ARGS

graph = CG(transformer=T,transformer_args=T_args,text=text)

if L:
    print(graph.linearize(linearizer=L,linearizer_args=L_args))

if args.print_json:
    print(graph.to_json())

if args.display:
    graph.draw()

