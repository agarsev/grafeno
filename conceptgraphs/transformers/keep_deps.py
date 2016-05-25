from .base import Transformer as Base

default_deps = {
    'dobj': 'THEME',
    'iobj': 'ARG',
    'ncsubj': 'AGENT'
}

class Transformer (Base):

    def __init__ (self, dep_translate = default_deps, **kwds):
        super().__init__(**kwds)
        self.__deps = dep_translate.keys()
        self.__translate = dep_translate

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        p = self.nodes[pid]
        c = self.nodes[cid]
        if 'concept' in p and 'concept' in c:
            edge['functor'] = self.__translate.get(dep, 'NONE')
        return edge
