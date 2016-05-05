from .base import Transformer as Base

default_attach = { 'ncmod' }

class Transformer (Base):

    def __init__ (self, attached_deps = default_attach, **kwds):
        super().__init__(**kwds)
        self.attached_deps = attached_deps

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        if dep in self.attached_deps and 'concept' in parent and 'concept' in child:
            parent['concept'] = child['concept']+'_'+parent['concept']
            del child['concept']
            del edge['functor']
        return edge
