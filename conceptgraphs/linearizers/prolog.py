from .semtriplets import Linearizer as Triplets

prolog_header = ':- multifile r/4, neg/4, arc/5, rule/6, frame/6, integrity/3.\n\n'

class Linearizer (Triplets):

    def __init__ (self, main_entity=None, **kwds):
        super().__init__(header=prolog_header, **kwds)
        if main_entity is None:
            main_entity = max((n['id'] for n in self.graph.nodes() if
                n.get('sempos')=='n'),
                key=lambda n: len(self.graph.edges(n)))
        self.main_entity = self.graph._g.node[main_entity]['concept']

    def process_node (self, n):
        try:
            return "r("+','.join([self.main_entity,
                n['left'], n['concept'], n['right']])+")."
        except KeyError:
            return None
