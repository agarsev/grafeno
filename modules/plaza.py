from .pos_extract import Transformer as PosExtract
from .sentence_record import Transformer as SentRecord
from .extend import Transformer as Extend
from .similarity_link import Transformer as SimLink

class Transformer (SimLink, Extend, SentRecord, PosExtract):

    def __init__ (self, **kwds):
        super().__init__(sempos={'noun':'n'}, **kwds)

    def pre_process (self, tree, graph):
        super().pre_process(tree, graph)
        self.reused_nodes = []

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if not 'synset' in sem:
            return None
        concept = sem.get('concept')
        # Only one node for each concept
        if concept in self.node_from_concept:
            self.reused_nodes.append(self.node_from_concept[concept])
            return None
        return sem

    def post_insertion (self, sentence_nodes, graph):
        super().post_insertion(sentence_nodes, graph)
        self.sentences[-1] += self.reused_nodes
        # Record the concept nodes
        for n in sentence_nodes:
            concept = graph._g.node[n]['concept']
            self.node_from_concept[concept] = n
