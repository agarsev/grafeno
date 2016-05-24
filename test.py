#!/usr/bin/env python3

import argparse
import yaml

import conceptgraphs.pipeline as pipeline

arrayize = lambda t: t.split(',')

arg_parser = argparse.ArgumentParser(description='Test script')
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-s','--string')
group.add_argument('-f','--file',type=argparse.FileType('r'))
arg_parser.add_argument('-t','--transformers',type=arrayize,help='transformer pipeline to use')
arg_parser.add_argument('-l','--linearizers',type=arrayize,help='linearizing pipeline to use')
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
else:
    config = {}
    if args.transformers:
        config['transformers'] = args.transformers
    if args.linearizers:
        config['linearizers'] = args.linearizers

config['text'] = text

result = pipeline.run(config)

if args.print_json:
    print(result.to_json())

if args.display:
    result.draw()

if not args.print_json or not args.display:
    print(result)
