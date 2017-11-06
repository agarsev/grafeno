from grafeno.transformers.base import Transformer as Base

preposition_pos = ('preposition', 'adp')

class Transformer (Base):
    '''Processes prepositions, trying to turn them into ``COMP`` edges with the
    preposition lemma as the ``class`` grammateme.

    These edges join the prepositional phrase nucleus (direct dependent of the
    preposition, head) with the parent (direct dominating node of the
    preposition).'''

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if msnode.get('pos') in preposition_pos:
            sem['pval'] = msnode.get('lemma')
        return sem

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        p = self.nodes[edge['parent']]
        c = self.nodes[edge['child']]
        if 'pval' in p:
            p['p_obj'] = edge
        if 'pval' in c:
            edge['functor'] = 'COMP'
            edge['class'] = c['pval']
            edge['pval'] = c['pval']
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
