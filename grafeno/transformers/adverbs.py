from grafeno.transformers.pos_extract import Transformer as PosExtract

adverbial_deps = ('ncmod', 'amod', 'advmod')

class Transformer (PosExtract):
    '''Processes adverbial modification as ``ATTR``.'''

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        c = self.nodes[child]
        if dep in adverbial_deps and 'concept' in p and 'concept' in c and c.get('sempos') == 'r':
            edge['functor'] = 'ATTR'
        return edge
