from grafeno.linearizers.base import Linearizer as Base

class Linearizer (Base):

    def __init__ (self, form='form', attrs=[], **kwds):
        super().__init__(separator='\n', **kwds)
        self.__analyzer_form = form
        self.__analyzer_attrs = attrs

    def get_root_nodes (self):
        return [n['id'] for n in self.graph.nodes()]

    def process_node (self, n):
        s = n[self.__analyzer_form]
        sep = ": "
        for attr in self.__analyzer_attrs:
            s += sep + n.get(attr, '-')
            sep = ", "
        return s
