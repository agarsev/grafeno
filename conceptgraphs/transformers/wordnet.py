from nltk.corpus import wordnet as wn

from .base import Transformer as Base

class Transformer (Base):

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        concept = sem.get('concept')
        if not concept:
            return sem
        pos = sem.get('sempos', 'n')
        if pos not in {'n','v'}:
            return sem
        ss = wn.synsets(concept, pos)
        if len(ss):
            # WSD by MFS
            sem['synset'] = ss[0]
        return sem
