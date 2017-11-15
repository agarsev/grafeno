from grafeno.linearizers.base import Linearizer as Base

class Linearizer (Base):

    def get_root_nodes (self):
        return [n['id'] for n in self.graph.nodes() if n.get('sempos')=='v']

    def expand_node (self, n):
        exps = super().expand_node(n)
        ret = []
        for n in exps:
            nes = self.graph.edges(n['id'])
            sempos = n.get('sempos')
            if sempos == 'v':
                subj = []
                dobj = []
                cc = []
                for m in nes:
                    ftor = nes[m]['functor']
                    if ftor == 'AGENT':
                        subj = [m]
                    elif ftor == 'THEME':
                        dobj = [m]
                    elif ftor == 'COMP':
                        cc += [{'expanded':True, 'concept':nes[m]['pval']}, m]
                ret += subj + [n] + dobj + cc + [{'expanded':True,
                    'punct': True, 'concept': '.'}]
            elif sempos == 'n':
                mod = []
                for m in nes:
                    if nes[m]['functor'] == 'ATTR':
                        mod = [m] + mod
                ret += mod + [n]
        return ret

    def process_node (self, n):
        word = super().process_node(n)
        sempos = n.get('sempos')
        if sempos == 'n':
            if n.get('num') == 'p':
                word += 's'
        return word.replace('_', ' ')

    def boundary (self, left, n, word, right):
        word = super().boundary(left, n, word, right)
        if not left or left.get('punct'):
            word = word[0].upper()+word[1:]
        if left and not n.get('punct'):
            word = ' '+word
        return word
