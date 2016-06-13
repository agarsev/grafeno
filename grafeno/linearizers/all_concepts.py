from grafeno.linearizers.base import Linearizer as Base

class Linearizer (Base):

    def __init__ (self, **kwds):
        super().__init__(separator=', ', **kwds)

    def get_root_nodes (self):
        return [n['id'] for n in self.graph.nodes()]
