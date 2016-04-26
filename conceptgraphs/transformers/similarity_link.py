from .sentence_record import Transformer as SentRecord
from .wordnet_get import Transformer as WNGet

from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

class Transformer (WNGet, SentRecord):

    def __init__ (self, sim_threshold = 0.01, sim_weight = 1, **kwds):
        super().__init__(**kwds)
        self.sim_threshold = sim_threshold
        self.sim_weight = sim_weight

    def post_insertion (self, sentence_nodes, graph):
        super().post_insertion(sentence_nodes, graph)
        g = graph._g
        threshold = self.sim_threshold
        weight = self.sim_weight
        oldnodes = set(n for s in self.sentences for n in s)
        for n in sentence_nodes:
            for m in oldnodes:
                if m == n:
                    continue
                ga = g.node[n]['gram']
                gb = g.node[m]['gram']
                if 'synset' not in ga or 'synset' not in gb \
                        or ga.get('sempos','x') != gb.get('sempos','-'):
                    continue
                sa = ga.get('synset')
                sb = ga.get('synset')
                sim = sa.jcn_similarity(sb, brown_ic)
                if sim > threshold:
                    graph.add_edge(n, m, 'SIM', {'weight':weight})
                    graph.add_edge(m, n, 'SIM', {'weight':weight})
