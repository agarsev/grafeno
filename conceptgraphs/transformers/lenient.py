from .base import Transformer as Base

class Transformer (Base):

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            try:
                p = self.nodes[edge['parent']].get('concept')
            except KeyError:
                p = True
            try:
                c = self.nodes[edge['child']].get('concept')
            except KeyError:
                c = True
            if (not p or not c) and 'functor' in edge:
                del edge['functor']
