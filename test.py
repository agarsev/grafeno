#!/usr/bin/env python3

import argparse
from bottle import abort, error, post, request, run

from conceptgraphs import Graph as CG
from conceptgraphs.transformers import get_pipeline

arg_parser = argparse.ArgumentParser(description='Test script')
arg_parser.add_argument('text')
arg_parser.add_argument('-t','--transformers',action='append',help='transformer pipeline to use')
arg_parser.add_argument('-p','--print-json',action='store_true',help='print json instead of displaying')
args = arg_parser.parse_args()

text = args.text
trans = args.transformers
T = get_pipeline(trans)
graph = CG(transformer=T,transformer_args={},text=text)

if args.print_json:
    print(graph.to_json())
else:
    graph.draw()
