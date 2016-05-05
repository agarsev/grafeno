from .base import Transformer as Base

default_reverse = { 'ncsubj' }

class Transformer (Base):

    def __init__ (self, reversed_deps = default_reverse, **kwds):
        super().__init__(**kwds)
        self.reversed_deps = reversed_deps

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        child = child.get('dep_rise', child)
        parent = parent.get('dep_lower', parent)
        if 'concept' not in child or 'concept' not in parent:
            if 'concept' not in parent:
                parent['dep_rise'] = child
            if 'concept' not in child:
                child['dep_lower'] = parent
            return edge
        if dep in self.reversed_deps:
            edge['parent'], edge['child'] = child['id'], parent['id']
        else:
            edge['parent'], edge['child'] = parent['id'], child['id']
        edge['functor'] = dep
        return edge
