from grafeno.transformers.base import Transformer as Base

class Transformer (Base):
    '''Processes copulative verbs, changing the functor of all its arguments to
    the same value: `COP'. This reflects the simmetry of copulative relations,
    so the resulting graph is independent of the surface expression.'''

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        p = self.nodes[edge['parent']]
        if p.get('concept','') == 'be':
            edge['functor'] = 'COP'
        return edge

