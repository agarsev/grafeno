from collections import namedtuple
from .functor import Functor

class TGrammar:

    def transform_tree(self, tree):
        return None

    def link_sentences(self, head1, head2):
        return None


# Tnodes are 3-tuples of:
# - head: dictionary. Syntactic features and already processed
#       grammatemes. `concept` should have the tectogrammatical lemma.
#       If no concept is found in the end, the node is dropped.
# - function: dictionary. In `fun` is the syntactic dependency, in
#       `functor` should be the Functor. Other attributes are grammatemes
#       of the dependency.
#       If no functor is found in the end, the edge and children are dropped.
# - children: list of Tnodes
TNode = namedtuple('TNode', ['head', 'function', 'children'])


# Each rule should take a Tnode and return a Tnode partially processed in the
# transform method. This method gets called only if the match method returns
# true.
TRule = namedtuple('TRule', ['match', 'transform'])


class IterativeRuleGrammar(TGrammar):

    def __init__ (self, transform_rules = [], link_rules = []):
        self.trules = transform_rules
        self.lrules = link_rules

    def __transform_node (self, tree, node, function, tokenmap):
        '''Take a dependency node and process it according to the rules'''
        children = []
        if 'children' in node:
            for child in node['children']:
                tnode = self.__transform_node(tree, child, child["function"], tokenmap)
                if tnode != None:
                    children.append(tnode)

        tn = TNode(
            head=tokenmap[node['token']].copy(),
            function={ 'fun': function },
            children=children)

        for r in self.trules:
            if r.match(tn):
                tn = r.transform(tn)

        if 'concept' not in tn.head:
            return None
        children = [c for c in tn.children if 'functor' in c.function]

        return TNode(tn.head, tn.function, children)


    def transform_tree (self, tree):
        '''Take a dependency tree extracted from Freeling and extract the conceptual graph'''
        tokenmap = { t['id']: t for t in tree['tokens'] }
        return self.__transform_node(tree, tree['dependencies'][0], 'top', tokenmap)


    def link_sentences (self, head1, head2):
        for l in self.lrules:
            f = l(head1, head2)
            if f:
                return f
        return None, None

