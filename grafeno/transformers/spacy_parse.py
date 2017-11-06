from grafeno.transformers.base import Transformer as Base

import spacy

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__nlp = spacy.load(self.lang)

    def parse_text (self, text):
        parse = self.__nlp(text)
        return parse.sents

    def transform_tree (self, tree):
        self.__process_node(tree.root)

    def __process_node (self, token):
        temp_id = '_t_{}'.format(token.i)
        self.__current_temp_id = temp_id
        self.nodes[temp_id] = self.transform_node({
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'spacy_tok': token
        })
        for c in token.children:
            c_id = self.__process_node(c)
            try:
                self.edges.append(self.transform_dep(c.dep_, temp_id, c_id))
            except KeyError:
                continue
        return temp_id

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        sem['id'] = self.__current_temp_id
        return sem

