from grafeno.transformers.base import Transformer as Base

class Transformer (Base):
    '''Utility class with useful methods'''

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__i = 0

    def sprout (self, nid, functor_or_edge, concept_or_node):
        new_id = nid+'__'+str(self.__i)
        self.__i += 1
        try:
            concept_or_node['id'] = new_id
        except TypeError:
            concept_or_node = { 'id':new_id, 'concept':concept_or_node }
        try:
            functor_or_edge.update({ 'parent':nid, 'child':new_id })
        except AttributeError:
            functor_or_edge = { 'parent':nid, 'child':new_id, 'functor':functor_or_edge }
        self.nodes[new_id] = concept_or_node
        self.edges.append(functor_or_edge)
        return new_id
