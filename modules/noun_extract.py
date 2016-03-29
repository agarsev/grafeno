from conceptgraphs.grammar import TRule, TNode, IterativeRuleGrammar as IRG
from conceptgraphs import Functor

def make_chain (tlist):
    if len(tlist)<1:
        return []
    else:
        up = tlist[0]
        return [TNode(up.head, up.function,
            children=up.children+make_chain(tlist[1:]))]

def pickup_nouns (tnode):
    if 'tag' in tnode.head and tnode.head['tag'][0] == 'N':
        return TNode(head={'concept':tnode.head['lemma'],'sempos':'N'},
                function={'functor':Functor.JUX},
                children=make_chain(tnode.children))
    elif len(tnode.children)>0:
        return make_chain(tnode.children)[0]
    else:
        return tnode

extract_nouns = TRule(
    match=lambda x: True,
    transform=pickup_nouns)

grammar = IRG(
    transform_rules=[extract_nouns],
    link_rules=[]
    )
