from grafeno.linearizers.triplets import Linearizer as Triplets

prolog_header = ':- multifile r/4, neg/4, arc/5, rule/6, frame/6, integrity/3.\n\n'

class Linearizer (Triplets):

    def __init__ (self, **kwds):
        super().__init__(header=prolog_header, **kwds)
        try:
            self.__me = self.graph.gram['main_entity']
        except KeyError:
            self.__me = max((n['id'] for n in self.graph.nodes() if
                n.get('sempos')=='n'),
                key=lambda n: len(self.graph.edges(n)))
        self.__main_concept = self.graph.node[self.__me]['concept']

    def process_node (self, n):
        try:

            return "r("+','.join([self.__main_concept,
                n['left'], n['concept'], n['right']])+")."
        except KeyError:
            return None
