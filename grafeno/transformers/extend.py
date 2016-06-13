from collections import deque
from nltk.corpus import wordnet as wn

from grafeno.transformers.index import Transformer as Index
from grafeno.transformers.wordnet import Transformer as WNGet

class Transformer (WNGet, Index):

    def __init__ (self, min_depth = 4, **kwds):
        super().__init__(**kwds)
        self.min_depth = min_depth

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph
        node_dict = self.node_from_concept
        # Extend with hypernyms
        to_extend = deque(sentence_nodes)
        while len(to_extend)>0:
            n = to_extend.popleft()
            node = g.node[n]
            ss = node.get('synset')
            if not ss:
                continue
            for cc in ss.hypernyms() + ss.instance_hypernyms():
                depth = ss.min_depth()
                if depth < self.min_depth:
                    continue
                concept = cc.lemmas()[0].name()
                if concept not in node_dict:
                    nid = g.add_node(concept,synset=cc)
                    to_extend.append(nid)
                    node_dict[concept] = nid
                else:
                    nid = node_dict[concept]
                g.add_edge(n, nid, 'HYP', weight=depth/(depth+1))
