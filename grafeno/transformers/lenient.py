from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            try:
                if 'parent' in edge:
                    p = edge['parent']
                    if p in self.nodes:
                        if 'concept' not in self.nodes[p]:
                            del edge['functor']
                    elif p not in self.graph.node:
                        del edge['functor']
                else:
                    del edge['functor']
                if 'child' in edge:
                    c = edge['child']
                    if c in self.nodes:
                        if 'concept' not in self.nodes[c]:
                            del edge['functor']
                    elif c not in self.graph.node:
                        del edge['functor']
                else:
                    del edge['functor']
            except KeyError as e:
                pass
