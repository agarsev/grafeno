from .pos_extract import Transformer as PosExtract

default_attach = { 'ncmod' }

class Transformer (PosExtract):

    def __init__ (self, attached_deps = default_attach, **kwds):
        super().__init__(**kwds)
        self.attached_deps = attached_deps

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        c = self.nodes[child]
        if dep in self.attached_deps and 'concept' in p and 'concept' in c and p.get('sempos') == 'n' and c.get('sempos') == 'j':
            p['concept'] = c['concept']+'_'+p['concept']
            del c['concept']
            return {}
        return edge
