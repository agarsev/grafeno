from .unique import Transformer as Unique
from .pos_extract import Transformer as PosExtract

class Transformer (Unique, PosExtract):

    def __init__ (self, **kwds):
        super().__init__(unique_sempos={'n',}, **kwds)

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if sem.get('concept') == 'be':
            sem['concept'] = 'is'
        return sem

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        if 'concept' not in parent or 'concept' not in child:
            return edge
        if dep == 'ncsubj':
            parent['id'] = child['id']
            if 'dobj' in parent:
                edge['functor'] = parent['concept']
                edge['parent'] = child['id']
                edge['child'] = parent['dobj']
            parent['verb_lemma'] = parent['concept']
            del parent['concept']
        if dep == 'dobj':
            if parent.get('verb_lemma'):
                edge['functor'] = parent['verb_lemma']
            else:
                parent['dobj'] = child['id']
        return edge
