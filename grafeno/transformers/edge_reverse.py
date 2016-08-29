from grafeno.transformers.base import Transformer as Base

default_reverse = { 'AGENT', }

class Transformer (Base):
    '''Reverses the direction of some edges.

    Parameters
    ----------
    reversed_edges : set
        Set of functors which should have reverse orientation from the syntactic
        dependency.
    '''

    def __init__ (self, reversed_edges = default_reverse, **kwds):
        super().__init__(**kwds)
        self.__functors = reversed_edges

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        if edge.get('functor') in self.__functors:
            edge['parent'], edge['child'] = edge['child'], edge['parent']
        return edge
