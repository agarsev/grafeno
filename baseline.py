#!/usr/bin/env python3

import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def get_full_sentences (text):
    return tokenizer.tokenize(text, realign_boundaries=True)

if __name__ == "__main__":

    import argparse, sys, importlib

    arg_parser = argparse.ArgumentParser(description='Baseline summary by extraction method')

    arg_parser.add_argument('fulltext', type=argparse.FileType('r'), help='Text file with the original text')
    arg_parser.add_argument('--length',type=int,default=100,help='Approximate number of words for the summary to have')
    arg_parser.add_argument('--margin',type=int,default=10,help='Upper margin for the length of the summary')

    args = arg_parser.parse_args()

    text = args.fulltext.read()
    full = get_full_sentences(text)

    length = 0
    last = 0
    while length < args.length:
        length += len(full[last].split(' '))
        if length < args.length + args.margin:
            last += 1
    print('\n'.join(full[:last]))
