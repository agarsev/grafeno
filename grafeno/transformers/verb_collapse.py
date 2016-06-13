from grafeno.transformers.pos_extract import Transformer as PosExtract

default_main_argument = [ 'dobj', 'iobj', 'ncmod' ]

class Transformer (PosExtract):

    def __init__ (self, sempos={}, main_argument=default_main_argument, **kwds):
        sempos['verb'] = 'v'
        super().__init__(sempos=sempos, **kwds)
        self.__main = main_argument

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[parent]
        if p.get('sempos') == 'v':
            if dep == 'ncsubj':
                p['relation'] = edge
                edge['functor'] = p.get('concept')
                edge['child'], edge['parent'] = edge['parent'], edge['child']
            elif dep in self.__main:
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
                for rel in self.__main:
                    if rel in a:
                        first_arg = a[rel]
                        break
                else:
                    del node['concept']
                    continue
                if 'functor' in first_arg and 'relation' in node:
                    node['relation']['functor'] += '_'+first_arg['functor']
                self.merge(first_arg['child'], nid)
