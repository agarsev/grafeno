from nltk.corpus import wordnet as wn

from grafeno.transformers.base import Transformer as Base

wordnet_langs = {
    'en': 'eng',
    'es': 'spa',
    'ca': 'cat'
}

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.wnlang = wordnet_langs[self.lang]

    def post_process (self):
        super().post_process()
        for n in self.nodes.values():
            concept = n.get('concept')
            if not concept:
                continue
            pos = n.get('sempos')
            if pos in {'n','v'}:
                ss = wn.synsets(concept, pos, lang=self.wnlang)
            elif pos == 'j':
                ss = wn.synsets(concept, 'a', lang=self.wnlang)
            else:
                ss = wn.synsets(concept, lang=self.wnlang)
            if len(ss):
                # WSD by MFS
                n['synset'] = ss[0]
