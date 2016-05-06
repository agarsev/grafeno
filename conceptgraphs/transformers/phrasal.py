from .semantic import Transformer as Semantic

class Transformer (Semantic):

    def post_process (self, nodes, edges):
        nodes, edges = super().post_process(nodes, edges)
        for nid in nodes:
            n = nodes[nid]
            if n.get('sempos') == 'v':
                has_theme = False
                for e in edges:
                    if e['parent'] == n['id'] and e.get('functor') == 'THEME':
                        has_theme = True
                if has_theme:
                    continue
                for e in edges:
                    if e['parent'] == n['id'] and e.get('functor') == 'COMP':
                        n['concept'] += '_'+e['pval']
                        del e['pval']
                        e['functor'] = 'THEME'
                        break
        return nodes, edges

