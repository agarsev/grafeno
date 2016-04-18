from conceptgraphs.transformer import Transformer as Base

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.sentences = []

    def post_insertion (self, sentence_nodes, graph):
        super().post_insertion(sentence_nodes, graph)
        self.sentences.append(sentence_nodes)
