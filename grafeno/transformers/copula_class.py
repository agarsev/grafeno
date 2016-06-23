from collections import defaultdict
import re

from grafeno.transformers.wordnet import Transformer as WordNet

abstract = { 'color': 'color',
    'colour': 'color',
    'size': 'size',
    'shape': 'shape',
    'appearance': 'appearance',
    'time': 'time',
    'times': 'time',
}

def get_class (synset):
    votes = defaultdict(lambda:0)
    for w in re.split('\W+', synset.definition()):
        if w in abstract:
            votes[abstract[w]]+=1
    if len(votes.keys()):
        cl = max(votes.keys(), key=lambda c: votes[c])
        if votes[cl]>0:
            return cl
    return None

class Transformer (WordNet):

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            if edge.get('functor') != 'ATTR' or 'class' in edge:
                continue
            c = edge['child']
            if c in self.nodes:
                c = self.nodes[c]
            elif c in self.graph.node:
                c = self.graph.node[c]
            else:
                continue
            cl = get_class(c['synset']) if 'synset' in c else None
            if cl:
                edge['class'] = cl
