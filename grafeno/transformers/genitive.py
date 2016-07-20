from grafeno.transformers.__utils import Transformer as Utils

class Transformer (Utils):
    '''Processes genitive relations. Does two main things:

    1. Turns saxon genitive (``'s``) into the preposition ``of`` with the
    correct dependencencies. This means that it must appear before preposition
    processing nodes in the transformer chain.
    2. If enabled, collapses ``of`` edges, adding the information to the parent
    node.

    Parameters
    ----------
    attach_genitive : bool
        If True, the concept is attached to the parent concept. For example,
        ``john's father`` turns into a single node ``father_of_john``, instead of a
        ``father`` node with an ``of`` edge to a ``john`` node.
    add_genitive_class : bool
        If both `attach_genitive` and `add_genitive_class` are True, a ``HYP``
        edge is added with the original dependent concept.
    '''

    def __init__ (self, attach_genitive = False, add_genitive_class = True, **kwds):
        super().__init__(**kwds)
        self.__gen_attach = attach_genitive
        self.__gen_addclass = add_genitive_class

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
        if 'genitive_obj' in c and p.get('sempos') != 'v' and 'concept' in p and self.__gen_attach:
            if self.__gen_addclass:
                self.sprout(parent, 'HYP', {'concept':p['concept'], 'sempos':p.get('sempos')})
            p['concept'] += '_of_' + c['genitive_obj']
        return edge
