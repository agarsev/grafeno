from itertools import product
import pexpect

from grafeno.transformers.sentences import Transformer as SentRecord
from grafeno.transformers.wordnet import Transformer as WNGet

class Transformer (WNGet, SentRecord):

    def __init__ (self, sim_threshold = 100, sim_weight = 1, **kwds):
        super().__init__(**kwds)
        self.__threshold = sim_threshold
        self.__weight = sim_weight
        self.__child = pexpect.spawn("/usr/bin/env WNSEARCHDIR=/usr/share/wordnet similarity.pl --type WordNet::Similarity::lesk --interact")
        self.__child.delaybeforesend = 0

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph
        threshold = self.__threshold
        weight = self.__weight
        child = self.__child
        oldnodes = set(n for s in g.gram['sentences'] for n in s)
        for n, m in product(sentence_nodes, oldnodes):
            if m == n:
                continue
            sa = g.node[n]['concept']
            sb = g.node[m]['concept']
            child.expect("Concept #1:")
            child.sendline(sa)
            child.expect("Concept #2:")
            child.sendline(sb)
            match = child.expect([' ([0-9.]+)\r\n', 'not found'])
            if match == 0:
                sim = int(child.match.group(1))
                if sim > threshold:
                    g.add_edge(n, m, 'SIM', weight=weight)
                    g.add_edge(m, n, 'SIM', weight=weight)
