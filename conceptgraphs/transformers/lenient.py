from .base import Transformer as Base

class Transformer (Base):

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            try:
                p = self.nodes[edge['parent']]['concept']
                c = self.nodes[edge['child']]['concept']
            except KeyError:
                if 'functor' in edge:
                    del edge['functor']
