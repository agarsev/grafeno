from .pos_extract import Transformer as PosExtract

class Transformer (PosExtract):

    def __init__ (self, sempos={}, **kwds):
        sempos['verb'] = 'v'
        super().__init__(sempos=sempos, **kwds)

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        if p.get('sempos') == 'v':
            if dep == 'ncsubj':
                p['relation'] = edge
                edge['functor'] = p.get('concept')
                edge['child'], edge['parent'] = edge['parent'], edge['child']
            else:
                try:
                    a = p['args']
                except KeyError:
                    a = dict()
                    p['args'] = a
                a[dep] = edge
        return edge

    def post_process (self):
        super().post_process()
        for nid, node in list(self.nodes.items()):
            if node.get('sempos') == 'v':
                try:
                    a = node['args']
                except KeyError:
                    del node['concept']
                    continue
                first_arg = a.get('dobj')
                if not first_arg:
                    _, first_arg = a.popitem()
                if 'functor' in first_arg:
                    node['relation']['functor'] += '_'+first_arg['functor']
                self.merge(first_arg['child'], nid)
