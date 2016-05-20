from .semantic import Transformer as Semantic

class Transformer (Semantic):

    def post_process (self):
        super().post_process()
        for nid, node in self.nodes.items():
            if node.get('sempos') == 'v':
                for e in self.edges:
                    if e.get('parent') == nid and e.get('functor') == 'THEME':
                        break
                else:
                    for e in self.edges:
                        # Find a prep complement to rise
                        if e.get('parent') == nid and e.get('functor') == 'COMP':
                            node['concept'] += '_'+e['pval']
                            del e['pval']
                            e['functor'] = 'THEME'
                            break

