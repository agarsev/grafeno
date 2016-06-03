from collections import defaultdict
import re

from .pos_extract import Transformer as PosExtract
from .__utils import Transformer as Utils

default_add_attached_class = True
default_retain_attachments = True

adj_classes = { 'color': 'color',
    'colour': 'color',
    'size': 'size',
    'shape': 'shape',
    'appearance': 'appearance',
    'quantity': 'quantity',
    'number': 'quantity',
    'time': 'time',
    'times': 'time',
}

def get_adj_class (synset):
    votes = defaultdict(lambda:0)
    for w in re.split('\W+', synset.definition()):
        if w in adj_classes:
            votes[adj_classes[w]]+=1
    if len(votes.keys()):
        cl = max(votes.keys(), key=lambda c: votes[c])
        if votes[cl]>0:
            return cl
    return None

class Transformer (PosExtract, Utils):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__addclass = kwds.get('add_attached_class', default_add_attached_class)
        self.__retain = kwds.get('retain_attachments', default_retain_attachments)

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        c = self.nodes[child]
        if dep == 'ncmod' and 'concept' in p and 'concept' in c and p.get('sempos') == 'n' and c.get('sempos') == 'j':
            if self.__addclass:
                self.sprout(parent, 'isa', {'concept':p['concept'], 'sempos':'n'})
            p['concept'] = c['concept']+'_'+p['concept']
            cl = get_adj_class(c['synset']) if 'synset' in c else None
            if cl:
                edge['functor'] = cl
            elif self.__retain:
                edge['functor'] = 'is'
            else:
                del c['concept']
        return edge
