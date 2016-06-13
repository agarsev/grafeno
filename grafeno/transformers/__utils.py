from grafeno.transformers.base import Transformer as Base

class Transformer (Base):
    '''Utility class with useful methods'''

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__i = 0

    def sprout (self, nid, functor, newsem):
        new_id = nid+'__'+str(self.__i)
        self.__i += 1
        newsem['id'] = new_id
        self.nodes[new_id] = newsem
        self.edges.append({ 'parent':nid, 'child':new_id, 'functor':functor })
