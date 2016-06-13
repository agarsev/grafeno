from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def transform_node (self, ms):
        sem = super().transform_node(ms)
        if ms.get('lemma') == 'not':
            sem['negation'] = True
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        parent = self.nodes[pid]
        child = self.nodes[cid]
        if 'negation' in child:
            if parent.get('sempos') == 'v' and 'concept' in parent:
                parent['concept'] = 'not_'+parent['concept']
            else:
                parent['negation'] = True
        if dep == 'aux' and child.get('concept') == 'not_do':
            parent['concept'] = 'not_'+parent['concept']
            del child['concept']
        return edge


