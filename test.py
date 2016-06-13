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
import yaml

from grafeno import pipeline

arrayize = lambda t: t.split(',')

arg_parser = argparse.ArgumentParser(description='Test script')
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-s','--string')
group.add_argument('-f','--file',type=argparse.FileType('r'))
arg_parser.add_argument('-t','--transformers',type=arrayize,help='transformer pipeline to use')
arg_parser.add_argument('-l','--linearizers',type=arrayize,help='linearizing pipeline to use')
arg_parser.add_argument('-c','--config-file',help='use a config file for pipeline options')
arg_parser.add_argument('-d','--display',action='store_true',help='display a drawing of the graph')
arg_parser.add_argument('-p','--print-json',action='store_true',help='print the graph in json')
args = arg_parser.parse_args()

if args.file:
    text = args.file.read()
else:
    text = args.string

if args.config_file:
    try:
        config_file = open('configs/'+args.config_file+'.yaml')
    except FileNotFoundError:
        config_file = None
    if not config_file:
        config_file = open(args.config_file)
    config = yaml.load(config_file)
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
