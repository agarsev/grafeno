from .base import Transformer as Base

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.graph.gram['sentences'] = []

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        self.graph.gram['sentences'].append(sentence_nodes[:])
