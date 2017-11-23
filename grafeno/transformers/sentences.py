from collections import deque

from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def __init__ (self, extended_sentence_edges = None, **kwds):
        super().__init__(**kwds)
        self.__ext = extended_sentence_edges
        self.graph.gram['sentences'] = []
        self.graph.gram['sentence_nodes'] = []

    def pre_process (self, tree):
        super().pre_process(tree)
        if self._parser == 'freeling':
            sent = []
            first = True
            for t in tree['tokens']:
                form = t['form'].replace('_', ' ')
                if form == '\s':
                    form = "'s"
                elif t.get('pos') != 'punctuation' and not first:
                    form = ' '+form
                first = False
                sent.append(form)
            text = ''.join(sent)
        elif self._parser == 'spacy':
            text = tree.text
        else:
            text = str(tree)
        self.graph.gram['sentences'].append(text)

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph._g
        ext = self.__ext
        if ext:
            record = set()
            to_extend = deque(sentence_nodes)
            while len(to_extend)>0:
                n = to_extend.popleft()
                if n in record:
                    continue
                record.add(n)
                for h in g[n]:
                    if g[n][h]['functor'] in ext:
                        to_extend.append(h)
            record = list(record)
        else:
            record = sentence_nodes[:]
        self.graph.gram['sentence_nodes'].append(record)
