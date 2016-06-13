from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.node_from_concept = dict()
        self.graph.gram['node_from_concept'] = self.node_from_concept
