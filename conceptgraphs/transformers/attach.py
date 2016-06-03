from .pos_extract import Transformer as PosExtract
from .__utils import Transformer as Utils

default_add_attached_class = True
default_retain_attachments = True

default_attach = { 'ncmod' }

class Transformer (PosExtract, Utils):

    def __init__ (self, attached_deps = default_attach, **kwds):
        super().__init__(**kwds)
        self.__addclass = kwds.get('add_attached_class', default_add_attached_class)
        self.__retain = kwds.get('retain_attachments', default_retain_attachments)
        self.attached_deps = attached_deps

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        c = self.nodes[child]
        if dep in self.attached_deps and 'concept' in p and 'concept' in c and p.get('sempos') == 'n' and c.get('sempos') == 'j':
            if self.__addclass:
                self.sprout(parent, 'isa', {'concept':p['concept'], 'sempos':'n'})
            p['concept'] = c['concept']+'_'+p['concept']
            if self.__retain:
                edge['functor'] = 'is'
            else:
                del c['concept']
        return edge
