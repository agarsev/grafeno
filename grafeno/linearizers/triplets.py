from grafeno.linearizers.base import Linearizer as Base

class Linearizer (Base):

    def __init__ (self, **kwds):
        super().__init__(separator='\n', **kwds)

    def get_root_nodes (self):
        return [n['id'] for n in self.graph.nodes()]

    def expand_node (self, n):
        exps = super().expand_node(n)
        ret = []
        nodes = self.graph.node
        for n in exps:
            nes = self.graph.edges(n['id'])
            for m in nes:
                ret.append({ 'expanded': True,
                    'left': n['concept'],
                    'concept': nes[m]['functor'],
                    'right': nodes[m]['concept'] })
        return ret

    def process_node (self, n):
        try:
            return n['concept']+'('+n['left']+','+n['right']+')'
        except KeyError:
            return None
