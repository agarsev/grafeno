from .wordnet import Transformer as WNGet

class Transformer (WNGet):

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        ss = sem.get('synset')
        if ss:
            concept_class = ss.lexname().split('.')[1]
            if concept_class and concept_class != 'Tops':
                cid = sem['id']+'_class'
                cc = { 'id': cid,
                    'concept': ss.lexname().split('.')[1] }
                if 'sempos' in sem:
                    cc['sempos'] = sem['sempos']
                self.nodes[cid] = cc
                self.edges.append({ 'parent': sem['id'],
                    'child': cid, 'functor': 'isa' })
        return sem
