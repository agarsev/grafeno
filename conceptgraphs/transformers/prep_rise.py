from .base import Transformer as Base

class Transformer (Base):

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if msnode.get('pos') == 'preposition':
            sem['pval'] = msnode.get('lemma')
        return sem

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[edge['parent']]
        c = self.nodes[edge['child']]
        if 'pval' in p:
            p['p_obj'] = edge
        if 'pval' in c:
            edge['functor'] = c['pval']
        return edge

    def post_process (self):
        super().post_process()
        for nid, node in list(self.nodes.items()):
            if 'pval' in node:
                try:
                    e = node['p_obj']
                except KeyError:
                    continue
                self.merge(e['child'], nid)
