from grafeno.linearizers.base import Linearizer as Base

class Linearizer (Base):

    def __init__ (self, make_comp_triplets = False, **kwds):
        super().__init__(separator='\n', **kwds)
        self.__use_comps = make_comp_triplets

    def get_root_nodes (self):
        return [n['id'] for n in self.graph.nodes() if n['sempos'] in {'v','n'}]

    def expand_node (self, n):
        exps = super().expand_node(n)
        ret = []
        nodes = self.graph.node
        for n in exps:
            nes = self.graph.edges(n['id'])
            sempos = n.get('sempos')
            ret.append(n)
            if sempos == 'v':
                for m in nes:
                    ftor = nes[m]['functor']
                    c = nodes[m]
                    if ftor == 'AGENT':
                        n['left'] = c['concept']
                    elif ftor == 'THEME':
                        n['right'] = c['concept']
                    elif ftor == 'COMP' and self.__use_comps:
                        ret.append({ 'expanded': True,
                            'concept': nes[m]['pval'],
                            'left': n['concept'],
                            'right': c['concept'] })
            elif sempos == 'n':
                for m in nes:
                    if nes[m]['functor'] == 'ATTR':
                        ret.append({ 'expanded': True,
                            'concept': 'is',
                            'left': n['concept'],
                            'right': nodes[m]['concept'] })
        return ret

    def process_node (self, n):
        try:
            return n['concept']+'('+n['left']+','+n['right']+')'
        except KeyError:
            return None
