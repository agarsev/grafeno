from .base import Transformer as Base

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.graph.gram['sentences'] = []
        self.graph.gram['sentence_nodes'] = []

    def pre_process (self, tree):
        super().pre_process(tree)
        sent = []
        first = True
        for t in tree['tokens']:
            form = t['form'].replace('_', ' ')
            if form == '\s':
                form = "'s"
            elif t['pos'] != 'punctuation' and not first:
                form = ' '+form
            first = False
            sent.append(form)
        self.graph.gram['sentences'].append(''.join(sent))

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        self.graph.gram['sentence_nodes'].append(sentence_nodes[:])
