from grafeno.transformers.base import Transformer as Base

DEF_POLARITY_GRAMMATEME = 'polarity'
DEF_POSITIVE = '+'
DEF_NEGATIVE = '-'

class Transformer (Base):
    '''Processes negation and its scope, setting the polarity of the affected
    verb.

    Parameters
    ----------
    polarity_grammateme : string
        Name of the grammateme to store polarity
    positive_polarity : string
        Value for the polarity grammateme when affirmative/positive
    negative_polarity : string
        Value for the polarity grammateme when negative
    '''

    def __init__ (self, polarity_grammateme=DEF_POLARITY_GRAMMATEME,
                  positive_polarity=DEF_POSITIVE, negative_polarity=DEF_NEGATIVE,
                  **kwds):
        super().__init__(**kwds)
        self.neg_gram = polarity_grammateme
        self.neg_pos = positive_polarity
        self.neg_neg = negative_polarity

    def transform_node (self, ms):
        '''Find negative particles, and by default mark all verbs as
        affirmative.'''
        sem = super().transform_node(ms)
        if ms.get('lemma') == 'not':
            sem['_negation'] = True
            if 'concept' in sem:
                del sem['concept']
        elif sem.get('sempos') == 'v':
            sem[self.neg_gram] = self.neg_pos
        return sem

    def transform_dep (self, dep, pid, cid):
        '''Rise negation until a verb is found, which is then marked negative.
        Modal negative particles are also processed.'''
        edge = super().transform_dep(dep, pid, cid)
        parent = self.nodes[edge['parent']]
        child = self.nodes[edge['child']]
        if '_negation' in child or dep=='neg':
            if parent.get('sempos') == 'v' and 'concept' in parent:
                parent[self.neg_gram] = self.neg_neg
            else:
                parent['_negation'] = True
        return edge

