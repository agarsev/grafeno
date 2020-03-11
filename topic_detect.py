"""
Uses clustering as used for summarization (see "Enriched Semantic Graphs for
Extractive Text Summarization, Antonio F. G. Sevilla, Alberto Fernández-Isabel,
Alberto Díaz, in The Conference of the Spanish Association for AI (CAEPIA 2016),
published by Springer in LNAI vol. 9868") but to extract the Hub Vertex Sets,
which can be seen as the main topics in the text.
"""
from grafeno import Graph as CG, transformers as tr
from grafeno.operations import operate

import argparse
arg_parser = argparse.ArgumentParser(description='Example topic detection script')
arg_parser.add_argument('file', type=argparse.FileType('r'))
arg_parser.add_argument('-l','--lang',help='language of the text', default='en')
args = arg_parser.parse_args()

T = tr.get_pipeline(['spacy_parse', 'pos_extract','thematic','phrasal','wordnet'])

g = CG(transformer=T, transformer_args={
    'lang': args.lang,
    'sempos': { 'noun': 'n' },
    'unique_gram': { 'hyper': [ True ] },
    'extended_sentence_edges': [ 'HYP' ]
    }, text=args.file.read())

g = operate(g, 'cluster', hubratio=0.2)

for hvs in g.gram['HVS']:
    keywords = set(g.node[n]['concept'] for n in hvs)
    print('Topic: {}'.format(', '.join(keywords)))
