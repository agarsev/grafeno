from itertools import product

from nltk.corpus import wordnet_ic
brown_ic = None

from grafeno.transformers.wordnet import Transformer as WNGet

class Transformer (WNGet):

    def __init__ (self, sim_threshold = 0.1, sim_weight = 1, **kwds):
        global brown_ic
        super().__init__(**kwds)
        if not brown_ic:
            brown_ic = wordnet_ic.ic('ic-brown.dat')
        self.__threshold = sim_threshold
        self.__weight = sim_weight

    def get_similarity (self, a, b):
        if 'synset' not in a or 'synset' not in b \
                or a.get('sempos','x') != b.get('sempos','-'):
            return 0
        sa = a['synset']
        sb = b['synset']
        return sa.jcn_similarity(sb, brown_ic)

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph
        threshold = self.__threshold
        weight = self.__weight
        oldnodes = set(g.node.keys())-set(sentence_nodes)
        for n, m in product(sentence_nodes, oldnodes):
            if m == n:
                continue
            sim = self.get_similarity(g.node[n], g.node[m])
            if sim > threshold:
                g.add_edge(n, m, 'SIM', weight=weight)
                g.add_edge(m, n, 'SIM', weight=weight)
