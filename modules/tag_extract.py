from conceptgraphs.grammar import TRule, TNode, IterativeRuleGrammar as IRG
from conceptgraphs import Functor

def make_chain (tlist):
    if len(tlist)<1:
        return []
    else:
        up = tlist[0]
        return [TNode(up.head, up.function,
            children=up.children+make_chain(tlist[1:]))]

def pickup_tagged (tnode, tags):
    if 'tag' in tnode.head and tnode.head['tag'][0] in tags:
        return TNode(head={'concept':tnode.head['lemma'],
                'sempos':tnode.head['tag'][0]},
                function={'functor':Functor.JUX},
                children=make_chain(tnode.children))
    elif len(tnode.children)>0:
        return make_chain(tnode.children)[0]
    else:
        return tnode

def extract_rule (tags):
    return TRule(
        match=lambda x: True,
        transform=lambda t: pickup_tagged(t, tags)
        )

def tag_extract (tags):
    return IRG(
        transform_rules=[extract_rule(tags)],
        link_rules=[])

grammar = tag_extract({'N'})
