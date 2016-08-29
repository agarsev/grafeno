from grafeno.transformers.base import Transformer as Base

class Transformer (Base):
    '''Removes edges where parent or child node don't have a concept.

    This might necessary because otherwise these edges would give an error when
    trying to be added to the graph. Ideally, this situation should never
    happen, but sometimes nodes get dropped after the edges have already been
    processed.'''

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
