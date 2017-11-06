from grafeno.transformers.pos_extract import Transformer as PosExtract
from grafeno.transformers.__utils import Transformer as Utils

adjective_deps = ('ncmod', 'amod')

class Transformer (PosExtract, Utils):
    '''Processes adjectives. Adds an ``ATTR`` functor relation to the head noun.

    Parameters
    ----------
    attach_adjectives : bool
        Attaches the adjectival concept to the head noun concept. Useful to
        distinguish nominal nodes when specified by modifiers.
    attached_adjective_hyper : bool
        If both `attach_adjectives` and `attached_adjective_hyper` are true, an
        hypernym node is added to the head with the original nominal concept.
    keep_attached_adj : bool
        If `attach_adjectives` is True and `keep_attached_adj` is False,
        adjectival nodes are dropped after being attached.
    '''

    def __init__ (self, attach_adjectives = False, attached_adjective_hyper = True, keep_attached_adj = False, **kwds):
        super().__init__(**kwds)
        self.__attach = attach_adjectives
        self.__hyper = attached_adjective_hyper
        self.__keep = keep_attached_adj

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        c = self.nodes[child]
        if (dep in adjective_deps or edge.get('functor')=='ATTR') and 'concept' in p and 'concept' in c and p.get('sempos') == 'n' and c.get('sempos') == 'j':
            if self.__attach:
                if self.__hyper:
                    self.sprout(parent, 'HYP', {'concept':p['concept'], 'sempos':'n'})
                p['concept'] = c['concept']+'_'+p['concept']
                if self.__keep:
                    edge['functor'] = 'ATTR'
                else:
                    del c['concept']
            else:
                edge['functor'] = 'ATTR'
        return edge
