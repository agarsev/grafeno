import pexpect

from .sentence_record import Transformer as SentRecord
from .wordnet_get import Transformer as WNGet

class Transformer (WNGet, SentRecord):

    def __init__ (self, sim_threshold = 100, sim_weight = 1, **kwds):
        super().__init__(**kwds)
        self.sim_threshold = sim_threshold
        self.sim_weight = sim_weight
        self.child = pexpect.spawn("/usr/bin/env WNSEARCHDIR=/usr/share/wordnet similarity.pl --type WordNet::Similarity::lesk --interact")
        self.child.delaybeforesend = 0

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes)
        g = self.graph
        threshold = self.sim_threshold
        weight = self.sim_weight
        child = self.child
        oldnodes = set(n for s in g.gram['sentences'] for n in s)
        for n in sentence_nodes:
            for m in oldnodes:
                sa = g._g.node[n]['concept']
                sb = g._g.node[m]['concept']
                child.expect("Concept #1:")
                child.sendline(sa)
                child.expect("Concept #2:")
                child.sendline(sb)
                match = child.expect([' ([0-9.]+)\r\n', 'not found'])
                if match == 0:
                    sim = int(child.match.group(1))
                    if sim > threshold:
                        g.add_edge(n, m, 'SIM', {'weight':weight})
                        g.add_edge(m, n, 'SIM', {'weight':weight})
