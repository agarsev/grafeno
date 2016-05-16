#!/usr/bin/env python3

import argparse
from bottle import abort, error, post, request, run

from conceptgraphs import Graph as CG, transformers, linearizers

arrayize = lambda t: t.split(',')

arg_parser = argparse.ArgumentParser(description='Test script')
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-s','--string')
group.add_argument('-f','--file',type=argparse.FileType('r'))
arg_parser.add_argument('-t','--transformers',type=arrayize,help='transformer pipeline to use',default=['semantic'])
arg_parser.add_argument('-l','--linearizers',type=arrayize,help='linearizing pipeline to use',default=[])
arg_parser.add_argument('-p','--print-json',action='store_true',help='print json instead of displaying')
args = arg_parser.parse_args()

if args.file:
    text = args.file.read()
else:
    text = args.string

T = transformers.get_pipeline(args.transformers)
graph = CG(transformer=T,transformer_args={},text=text)

if args.print_json:
    print(graph.to_json())
elif len(args.linearizers)>0:
    L = linearizers.get_pipeline(args.linearizers)
    print(graph.linearize(L))
else:
    graph.draw()

