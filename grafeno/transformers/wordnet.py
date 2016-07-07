from nltk.corpus import wordnet as wn

from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def post_process (self):
        super().post_process()
        for n in self.nodes.values():
            concept = n.get('concept')
            if not concept:
                continue
            pos = n.get('sempos')
            if pos in {'n','v'}:
                ss = wn.synsets(concept, pos)
            elif pos == 'j':
                ss = wn.synsets(concept, 'a')
            else:
                ss = wn.synsets(concept)
            if len(ss):
                # WSD by MFS
                n['synset'] = ss[0]
