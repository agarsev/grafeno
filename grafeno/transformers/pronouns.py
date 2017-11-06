from grafeno.transformers.base import Transformer as Base

# TODO:
# - check with spacy
# - reference across sentences (what to do with the dep?)
# - syntactic agreement
# - semantic agreement (heuristic)

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__last_noun = None

    def transform_node (self, ms):
        sem = super().transform_node(ms)
        if ms.get('pos') == 'noun':
            self.__last_noun = sem
        elif ms.get('pos') == 'pronoun' and self.__last_noun:
            if ms.get('type') == 'personal':
                sem['true_node'] = self.__last_noun
            elif ms.get('type') == 'possessive':
                ms['pos'] = 'preposition'
                ms['lemma'] = 'of'
                self.deps.append(('dobj', sem['id'], self.__last_noun['id']))
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        p = self.nodes[edge['parent']]
        c = self.nodes[edge['child']]
        if 'true_node' in p:
            edge['parent'] = p['true_node']['id']
        if 'true_node' in c:
            edge['child'] = c['true_node']['id']
        return edge
