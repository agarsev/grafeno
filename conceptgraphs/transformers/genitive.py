from .__utils import Transformer as Utils

default_add_genitive_class = True

class Transformer (Utils):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__addclass = kwds.get('add_genitive_class', default_add_genitive_class)

    def transform_node (self, ms):
        sem = super().transform_node(ms)
        if ms.get('pos') == 'preposition' and ms.get('lemma') == 'of':
            sem['genitive_of'] = True
        if ms.get('lemma') == '\s':
            ms['pos'] = 'preposition'
            ms['lemma'] = 'of'
            p_obj = self.__prev_node
            sem['genitive_obj'] = p_obj['concept']
            p_obj['true_parent'] = sem['id']
        self.__prev_node = sem
        return sem

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        c = self.nodes[edge['child']]
        if 'true_parent' in c:
            edge['parent'] = c['true_parent']
        p = self.nodes[edge['parent']]
        if 'genitive_of' in p and 'concept' in c:
            p['genitive_obj'] = c['concept']
        if 'genitive_obj' in c and p.get('sempos') != 'v' and 'concept' in p:
            if self.__addclass:
                self.sprout(parent, 'isa', {'concept':p['concept'], 'sempos':p.get('sempos')})
            p['concept'] += '_of_' + c['genitive_obj']
        return edge
