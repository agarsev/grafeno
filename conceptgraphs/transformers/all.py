from .base import Transformer as Base

class Transformer (Base):

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        sem.update(msnode)
        sem['concept'] = msnode['lemma']
        return sem

    def transform_dep (self, dependency, parent, child):
        edge = super().transform_dep(dependency, parent, child)
        edge['functor'] = dependency
        return edge
