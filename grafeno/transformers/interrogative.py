# TODO: rename to rel pronoun
from grafeno.transformers.pos_extract import Transformer as PosExtract

class Transformer (PosExtract):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.graph.questions = []

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        tag_pos = msnode.get('tag', msnode.get('pos'))
        if tag_pos and tag_pos.startswith('w'):
            sem['concept'] = '?'
            sem['sempos'] = 'n'
        return sem

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        for n in sentence_nodes:
            if self.graph.node[n]['concept'] == '?':
                self.graph.questions.append(n)

