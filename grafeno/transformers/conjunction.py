from grafeno.transformers.base import Transformer as Base

import copy

class Transformer (Base):

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        if dep == 'conj':
            p = self.nodes[edge['parent']]
            c = self.nodes[edge['child']]
            p['conj_siblings'] = p.get('conj_siblings', [])+[c]
        return edge

    def post_process (self):
        super().post_process()
        for conj_id, conj in self.nodes.items():
            if 'conj_siblings' not in conj:
                continue
            new_edges = []
            for s in conj['conj_siblings']:
                verb_conjunction = conj['sempos'] == 'v' and s['sempos'] == 'v'
                if verb_conjunction:
                    new_edges.append({'parent':conj_id,'child':s['id'],'functor':'SEQ'})
                for e in self.edges:
                    c_id = e.get('child', None)
                    p_id = e.get('parent', None)
                    # "Dominated" conjunction (duplicate nodes and dominating edges)
                    if c_id == conj_id:
                        new_edge = copy.deepcopy(e)
                        new_edge['child'] = s['id']
                        new_edges.append(new_edge)
                    # "Sequential" conjunction (between verbs)
                    if verb_conjunction and p_id == conj_id:
                        # TODO
                        # Copy edge iff functor in transferred ones (eg. agent,
                        # not theme) AND the sibling verb's corresponding
                        # function not filled
                        pass
            del conj['conj_siblings']
            self.edges.extend(new_edges)
