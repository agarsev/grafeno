from grafeno.transformers.base import Transformer as Base

class Transformer (Base):
    '''This transformer carries over all morphological nodes and syntactic
    dependencies to the semantic level. It is good for developing/debugging
    purposes, since it directly translates the dependency tree into the semantic
    graph.'''

    def transform_node (self, msnode):
        '''The concept is the lemma of the morphological node.'''
        sem = super().transform_node(msnode)
        sem.update(msnode)
        sem['concept'] = msnode['lemma']
        return sem

    def transform_dep (self, dependency, parent, child):
        '''The functor is the dependency name.'''
        edge = super().transform_dep(dependency, parent, child)
        edge['functor'] = dependency
        return edge
