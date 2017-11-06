# TODO: check with spacy
from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def transform_node (self, ms):
        sem = super().transform_node(ms)
        if ms.get('lemma','').isnumeric():
            sem['concept'] = ms['lemma']
            sem['sempos'] = 'j'
        elif sem.get('concept','').isnumeric():
            sem['concept'] = sem['concept']
        return sem

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        c = self.nodes[child]
        if dep == 'ncmod-num':
            edge['functor'] = 'ATTR'
            edge['class'] = 'number'
        return edge
