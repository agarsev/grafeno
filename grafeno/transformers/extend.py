from collections import deque
from nltk.corpus import wordnet as wn

from grafeno.transformers.wordnet import Transformer as WNGet
from grafeno.transformers.__utils import Transformer as Utils

class Transformer (WNGet, Utils):
    '''Adds to the graph all WordNet hypernyms of every possible concept node.

    The hypernyms are added as nodes with grammateme ``hyper = True'', and
    related by edges with functor ``HYP''.

    Parameters
    ----------
    extend_min_depth : int
        Minimum depth of hypernyms to add. This depth is defined as the shortest
        path from the synset to the root of the WordNet hypernym hierarchy.
    '''

    def __init__ (self, extend_min_depth = 4, **kwds):
        super().__init__(**kwds)
        self.__min_depth = extend_min_depth

    def post_process (self):
        super().post_process()
        g = self.graph
        mind = self.__min_depth
        # Extend with hypernyms
        to_extend = deque(list(self.nodes))
        while len(to_extend)>0:
            n = to_extend.popleft()
            node = self.nodes[n]
            ss = node.get('synset')
            if not ss:
                continue
            for cc in ss.hypernyms() + ss.instance_hypernyms():
                depth = ss.min_depth()
                if depth < mind:
                    continue
                concept = cc.lemmas()[0].name()
                nid = self.sprout(n,
                        {'functor':'HYP','weight':depth/(depth+1)},
                        {'concept':concept,'synset':cc,'hyper':True})
                to_extend.append(nid)
