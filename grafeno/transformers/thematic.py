from grafeno.transformers.pos_extract import Transformer as PosExtract

class Transformer (PosExtract):

    predication = {
            'ncsubj': ('AGENT', 1.0, {'n'}),
            'csubj': ('AGENT', 1.0, None),
            'nsubj': ('AGENT', 1.0, {'n'}),
            'agent': ('AGENT', 1.0, {'n'}),
            'dobj': ('THEME', 1.0, None),
            'nsubjpass': ('THEME', 1.0, {'n'}),
            'attr': ('THEME', 1.0, {'n'}),
            'iobj': ('IOBJ', 1.0, None),
            'prep': ('ARG', 1.0, None),
            'obj': ('ARG', 1.0, None),
            'obl': ('ARG', 1.0, None),
            }

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if sem.get('sempos') == 'v':
            sem['tense'] = msnode.get('vform')
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        p = self.nodes[edge['parent']]
        c = self.nodes[edge['child']]
        if not('concept' in p and 'concept' in c and p.get('sempos')=='v'):
            return edge
        if dep in self.predication:
            functor, w, pos_set = self.predication[dep]
            if not pos_set or c.get('sempos') in pos_set:
                edge['functor'], edge['weight'] = functor, w
        elif dep == 'aux' or dep == 'auxpass':
            mod = c['concept']
            if mod == 'have':
                p['aspect'] = 'perfect'
                del c['concept']
            elif mod == 'be':
                p['passive'] = True
                del c['concept']
        return edge

    def post_process (self):
        super().post_process()
        for nid, n in self.nodes.items():
            if n.get('passive'):
                for e in self.edges:
                    if e.get('parent') != nid:
                        continue
                    f = e.get('functor')
                    if f == 'AGENT':
                        e['functor'] = 'THEME'
                    if f == 'COMP' and e.get('class') == 'by':
                        e['functor'] = 'AGENT'
                        del e['class']
                        del e['pval']
                del n['passive']
