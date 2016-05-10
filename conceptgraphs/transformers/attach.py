from .pos_extract import Transformer as PosExtract

default_attach = { 'ncmod' }

class Transformer (PosExtract):

    def __init__ (self, attached_deps = default_attach, **kwds):
        super().__init__(**kwds)
        self.attached_deps = attached_deps

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        if dep in self.attached_deps and 'concept' in parent and 'concept' in child and parent.get('sempos') == 'n' and child.get('sempos') == 'j':
            parent['concept'] = child['concept']+'_'+parent['concept']
            del child['concept']
            if 'functor' in edge:
                del edge['functor']
        return edge
