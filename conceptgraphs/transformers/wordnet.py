from nltk.corpus import wordnet as wn

from .base import Transformer as Base

class Transformer (Base):

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        concept = sem.get('concept')
        if not concept:
            return sem
        pos = sem.get('sempos')
        if pos in {'n','v'}:
            ss = wn.synsets(concept, pos)
        elif pos == 'j':
            ss = wn.synsets(concept, 'a')
        else:
            ss = wn.synsets(concept)
        if len(ss):
            # WSD by MFS
            sem['synset'] = ss[0]
        return sem
