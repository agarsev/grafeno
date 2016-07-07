from grafeno.transformers.wordnet import Transformer as WNGet

class Transformer (WNGet):
    '''Finds the wordnet-defined `class' of a concept.

    Parameters
    ----------
    concept_class_hypernyms : bool
        If True, a new node is added with the class concept, related to the
        original node by an ``HYP'' edge.
    '''

    def __init__ (self, concept_class_hypernyms = True, **kwds):
        super().__init__(**kwds)
        self.__hyper = concept_class_hypernyms

    def post_process (self):
        super().post_process()
        for n in self.nodes.values():
            ss = n.get('synset')
            if ss:
                concept_class = ss.lexname().split('.')[1]
                if concept_class and concept_class != 'Tops':
                    n['class'] = concept_class
                    if self.__hyper:
                        chyp = { 'concept': concept_class }
                        if 'sempos' in n:
                            chyp['sempos'] = n['sempos']
                        self.sprout(n['id'], 'HYP', chyp)
