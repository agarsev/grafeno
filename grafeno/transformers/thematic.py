from grafeno.transformers.pos_extract import Transformer as PosExtract

class Transformer (PosExtract):

    predication = {
            'ncsubj': ('AGENT', 1.0, {'n'}),
            'dobj': ('THEME', 1.0, None),
            'iobj': ('IOBJ', 1.0, None),
            }

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        if sem.get('sempos') == 'v':
            sem['tense'] = msnode.get('vform')
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        parent = self.nodes[edge['parent']]
        child = self.nodes[edge['child']]
        if 'concept' not in parent or 'concept' not in child:
            return edge
        elif parent.get('sempos') == 'v' and dep in self.predication:
            functor, w, pos_set = self.predication[dep]
            if not pos_set or child.get('sempos') in pos_set:
                edge['functor'], edge['weight'] = functor, w
        return edge
