#!/usr/bin/env python3

from conceptgraphs import Graph as CG


if __name__ == "__main__":

    import argparse, sys

    arg_parser = argparse.ArgumentParser(description='Test new architecture')
    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')
    args = arg_parser.parse_args()

    text = args.fulltext.read()

    from modules.newgrammar import Grammar as Newgrammar
    graph = CG(grammar=Newgrammar(), text=text)
    from modules.simple_nlg import linearize
    print(linearize(graph))
