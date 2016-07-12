import pexpect

from grafeno.transformers.sim_link import Transformer as SimLink

class Transformer (SimLink):

    def __init__ (self, sim_threshold = 100, sim_weight = 1, **kwds):
        super().__init__(sim_threshold=sim_threshold, sim_weight=sim_weight, **kwds)
        self.__child = pexpect.spawn("/usr/bin/env WNSEARCHDIR=/usr/share/wordnet similarity.pl --type WordNet::Similarity::lesk --interact")
        self.__child.delaybeforesend = 0

    def get_similarity (self, a, b):
        child = self.__child
        sa = a['concept']
        sb = b['concept']
        child.expect("Concept #1:")
        child.sendline(sa)
        child.expect("Concept #2:")
        child.sendline(sb)
        match = child.expect([' ([0-9.]+)\r\n', 'not found'])
        return int(child.match.group(1)) if match == 0 else 0
