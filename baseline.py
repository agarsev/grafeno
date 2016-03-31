#!/usr/bin/env python3

from conceptgraphs import Graph as CG

from common import concept_coverage

from modules.tag_extract import tag_extract

if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Extract the first concepts from a text, and compute overlap on true summary.')
    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')
    arg_parser.add_argument('summary', type=argparse.FileType('r'), help='Text file with a correct summary')
    arg_nums = arg_parser.add_mutually_exclusive_group(required=True)
    arg_nums.add_argument('-n', '--number', type=int, help='Number of concepts to extract')
    arg_nums.add_argument('-r', '--ratio', type=float, help='Proportion of concepts to extract against the total number of concepts')
    args = arg_parser.parse_args()

    text = args.fulltext.read()
    summ = args.summary.read()

    graph = CG(grammar=tag_extract({'N','V','J','R'}), text=text)

    if args.number:
        number = args.number
    else:
        number = int(len(graph._g.nodes())*args.ratio)

    sub = graph._g.subgraph(graph._g.nodes()[:number])
    graph._g = sub

    print(concept_coverage(graph, summ))
