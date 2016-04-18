from collections import deque
from nltk.corpus import wordnet as wn

from .wordnet_get import Transformer as WNGet

class Transformer (WNGet):

    def __init__ (self, min_depth = 4, **kwds):
        super().__init__(**kwds)
        self.node_from_concept = dict()
        self.min_depth = 4

    def post_insertion (self, sentence_nodes, graph):
        super().post_insertion(sentence_nodes, graph)
        g = graph._g
        # Extend with hypernyms
        to_extend = deque(sentence_nodes)
        while len(to_extend)>0:
            n = to_extend.popleft()
            node = g.node[n]
            ss = node['gram'].get('synset')
            if not ss:
                continue
            for cc in ss.hypernyms() + ss.instance_hypernyms():
                depth = ss.min_depth()
                if depth < self.min_depth:
                    continue
                concept = cc.lemmas()[0].name()
                if concept not in self.node_from_concept:
                    nid = graph.add_node(concept,gram={'synset':cc,'sempos':'n'})
                    to_extend.append(nid)
                    self.node_from_concept[concept] = nid
                else:
                    nid = self.node_from_concept[concept]
                graph.add_edge(n, nid, 'HYP', {'weight':depth/(depth+1)})
