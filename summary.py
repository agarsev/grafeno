#!/usr/bin/env python3

from conceptgraphs import Graph as CG

if __name__ == "__main__":

    import argparse, sys

    arg_parser = argparse.ArgumentParser(description='Summarize text via concept graphs')
    arg_parser.add_argument('text', help='Text file to summarize')
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    arg_parser.add_argument('-l','--linearize',help="Linearizing module to use",default='simple_nlg')
    args = arg_parser.parse_args()

    sys.path.insert(1, 'modules')

    T = __import__(args.transform)
    cg = CG(grammar=T.grammar, text=args.text)
    cg.draw()
