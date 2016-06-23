from grafeno.transformers.semantic import Transformer as Semantic

class Transformer (Semantic):

    def post_process (self):
        super().post_process()
        for nid, node in self.nodes.items():
            if node.get('sempos') == 'v':
                for e in self.edges:
                    if e.get('parent') == nid and e.get('functor') == 'THEME':
                        break
                else:
                    # Find a prep complement to rise
                    for e in self.edges:
                        try:
                            pid, cpos, functor = e['parent'], self.nodes[e['child']]['sempos'], e['functor']
                        except KeyError:
                            continue
                        if pid == nid and functor == 'COMP' and cpos == 'n' and 'pval' in e:
                            node['concept'] += '_'+e['pval']
                            del e['pval']
                            e['functor'] = 'THEME'
                            break

