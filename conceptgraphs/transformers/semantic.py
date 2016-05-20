from .pos_extract import Transformer as PosExtract

class Transformer (PosExtract):

    predication = {
            'ncsubj': ('AGENT', 1.0, {'n'}),
            'dobj': ('THEME', 1.0, None),
            'iobj': ('IOBJ', 1.0, None),
            }

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        sempos = sem.get('sempos')
        if sempos == 'n':
            sem['proper'] = msnode.get('type') == 'proper'
            sem['num'] = msnode.get('num','p')
        elif sempos == 'v':
            sem['tense'] = msnode.get('vform')
        elif msnode.get('pos') == 'preposition':
            sem['pval'] = msnode.get('lemma')
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        parent = self.nodes[pid]
        child = self.nodes[cid]
        if 'pval' in child:
            edge['functor'] = 'COMP'
            edge['pval'] = child['pval']
        elif 'concept' not in parent or 'concept' not in child:
            return edge
        elif parent.get('sempos') == 'v' and dep in self.predication:
            functor, w, pos_set = self.predication[dep]
            if not pos_set or child.get('sempos') in pos_set:
                edge['functor'], edge['weight'] = functor, w
        elif parent.get('sempos') == 'n' and dep == 'ncmod':
            edge['functor'] = 'ATTR'
        return edge

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            try:
                p = self.nodes[edge['parent']]
            except KeyError:
                continue
            if 'pval' in p:
                self.merge(edge['child'], edge['parent'])
