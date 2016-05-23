from .wordnet import Transformer as WNGet

from itertools import product

from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

class Transformer (WNGet):

    def __init__ (self, sim_threshold = 0.1, sim_weight = 1, **kwds):
        super().__init__(**kwds)
        self.__threshold = sim_threshold
        self.__weight = sim_weight

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph
        threshold = self.__threshold
        weight = self.__weight
        oldnodes = set(g.node.keys())-set(sentence_nodes)
        for n, m in product(sentence_nodes, oldnodes):
            if m == n:
                continue
            ga = g.node[n]
            gb = g.node[m]
            if 'synset' not in ga or 'synset' not in gb \
                    or ga.get('sempos','x') != gb.get('sempos','-'):
                continue
            sa = ga.get('synset')
            sb = gb.get('synset')
            sim = sa.jcn_similarity(sb, brown_ic)
            if sim > threshold:
                g.add_edge(n, m, 'SIM', weight=weight)
                g.add_edge(m, n, 'SIM', weight=weight)
