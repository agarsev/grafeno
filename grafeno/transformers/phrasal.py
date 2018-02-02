from grafeno.transformers.thematic import Transformer as Thematic

class Transformer (Thematic):

    def __init__ (self, guess_phrasals = True, **kwds):
        super().__init__(**kwds)
        self.__guess = guess_phrasals

    def pre_process (self, tree):
        super().pre_process(tree)
        self.__first_prep = None

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if msnode['pos'] in ('particle', 'part'):
            sem['particle'] = msnode['lemma']
        elif msnode['pos'] == 'preposition' and not self.__first_prep:
            self.__first_prep = sem['id']
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        p = self.nodes[pid]
        c = self.nodes[cid]
        if dep in ('prt', 'ncmod-prt') and p.get('sempos') == 'v' and 'particle' in c:
            p['concept'] += '_'+c['particle']
        return edge

    def post_process (self):
        super().post_process()
        if self.__guess:
            for nid, node in self.nodes.items():
                if node.get('sempos') == 'v':
                    for e in self.edges:
                        if e.get('parent') == nid and e.get('functor') == 'THEME':
                            break
                    else:
                        # Guess and use the first prep complement as THEME
                        c = self.__first_prep
                        for e in self.edges:
                            if e.get('parent') != nid or e.get('functor') != 'COMP':
                                continue
                            if e.get('child') == c:
                                node['concept'] += '_'+e['pval']
                                del e['pval']
                                e['functor'] = 'THEME'
                                break
