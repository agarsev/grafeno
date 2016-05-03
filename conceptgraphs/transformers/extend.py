from collections import deque
from nltk.corpus import wordnet as wn

from .wordnet_get import Transformer as WNGet

class Transformer (WNGet):

    def __init__ (self, min_depth = 4, **kwds):
        super().__init__(**kwds)
        if not hasattr(self, 'node_from_concept'):
            self.node_from_concept = dict()
        self.min_depth = min_depth

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph
        # Extend with hypernyms
        to_extend = deque(sentence_nodes)
        while len(to_extend)>0:
            n = to_extend.popleft()
            node = g._g.node[n]
            ss = node['gram'].get('synset')
            if not ss:
                continue
            for cc in ss.hypernyms() + ss.instance_hypernyms():
                depth = ss.min_depth()
                if depth < self.min_depth:
                    continue
                concept = cc.lemmas()[0].name()
                if concept not in self.node_from_concept:
                    nid = g.add_node(concept,gram={'synset':cc,'sempos':'n'})
                    to_extend.append(nid)
                    self.node_from_concept[concept] = nid
                else:
                    nid = self.node_from_concept[concept]
                g.add_edge(n, nid, 'HYP', {'weight':depth/(depth+1)})
