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
        self.__start = 'r("'+self.__main_concept+'",'
        self.__end = ').'

    def process_node (self, n):
        try:
            triplet = [n['left'], n['concept'], n['right']]
            triplet = ['"'+t+'"' for t in triplet]
            return self.__start + ','.join(triplet) + self.__end
        except KeyError:
            return None
