#!/usr/bin/env python3

import argparse
from bottle import abort, error, post, request, run
import importlib

from conceptgraphs import Graph as CG
from conceptgraphs.transformers import get_pipeline

arg_parser = argparse.ArgumentParser(description='Test script')
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-s','--string')
group.add_argument('-f','--file',type=argparse.FileType('r'))
arg_parser.add_argument('-t','--transformers',action='append',help='transformer pipeline to use')
arg_parser.add_argument('-p','--print-json',action='store_true',help='print json instead of displaying')
arg_parser.add_argument('-l','--linearize',help='linearize the graph with the provided module')
args = arg_parser.parse_args()

if args.file:
    text = args.file.read()
else:
    text = args.string

trans = args.transformers
T = get_pipeline(trans)
graph = CG(transformer=T,transformer_args={},text=text)

if args.print_json:
    print(graph.to_json())
elif args.linearize:
    L = importlib.import_module(args.linearize).Linearizer
    print(graph.linearize(L))
else:
    graph.draw()

