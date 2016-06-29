from collections import defaultdict
import re

from grafeno.transformers.wordnet import Transformer as WordNet

DEFAULT_KEYWORDS = { 'color': 'color',
    'colour': 'color',
    'size': 'size',
    'shape': 'shape',
    'appearance': 'appearance',
    'time': 'time',
    'times': 'time',
}

class Transformer (WordNet):
    '''Specifies ``ATTR`` edges by trying to find the specific property name and
    adding it as a ``class`` grammateme. It relies on WordNet definitions.

    For example, if there is a ``SWAN -- ATTR --> BLUE`` edge, the ``class``
    attribute with value ``color`` will be added to it.

    Parameters
    ----------
    atribute_class_keywords : dict
        Specifies a non-default mapping from keywords to property class names.
        The class name with most keywords found in the WordNet definitions will
        be chosen.
    '''

    def __init__ (self, attribute_class_keywords = DEFAULT_KEYWORDS, **kwds):
        super().__init__(**kwds)
        self.__kwds = attribute_class_keywords


    def _get_class (self, synset):
        votes = defaultdict(lambda:0)
        for w in re.split('\W+', synset.definition()):
            if w in self.__kwds:
                votes[self.__kwds[w]]+=1
        if len(votes.keys()):
            cl = max(votes.keys(), key=lambda c: votes[c])
            if votes[cl]>0:
                return cl
        return None

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            if edge.get('functor') != 'ATTR' or 'class' in edge:
                continue
            c = edge['child']
            if c in self.nodes:
                c = self.nodes[c]
            elif c in self.graph.node:
                c = self.graph.node[c]
            else:
                continue
            cl = self._get_class(c['synset']) if 'synset' in c else None
            if cl:
                edge['class'] = cl
