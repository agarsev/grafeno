from conceptgraphs.grammar import TRule, TNode, IterativeRuleGrammar as IRG
from conceptgraphs import Functor

def match_tagclass (tnode, tagclass):
    return 'tag' in tnode.head and tnode.head['tag'][0] == tagclass

def noun_transform (tnode):
    children = []
    for c in tnode.children:
        if c.function['fun'] == 'ncmod':
            children.append(TNode(c.head, {'functor': Functor.ATTR}, c.children))
    return TNode(head={'concept':tnode.head['lemma'],'sempos':'N'},
                 function=tnode.function,
                 children=children)

extract_nouns = TRule(
    match=lambda t: match_tagclass(t, 'N'),
    transform=noun_transform)


def predicative_verbs (tnode):
    children = []
    for c in tnode.children:
        ftor = {}
        synt = c.function['fun']
        if synt == 'ncsubj':
            ftor['functor'] = Functor.AGENT
        elif synt == 'dobj':
            ftor['functor'] = Functor.THEME
        elif synt == 'PREP':
            ftor['functor'] = Functor.COMP
            ftor['pval'] = c.function['pval']
        children.append(TNode(c.head, ftor, c.children))
    return TNode(head={'concept':tnode.head['lemma'],'sempos':'V'},
                 function=tnode.function,
                 children=children)

extract_pverbs = TRule(
    match=lambda t: match_tagclass(t, 'V') and t.function != 'aux',
    transform=predicative_verbs)


def copula_transform (tnode):
    try:
        subj = next(c for c in tnode.children if c.function['fun']=='ncsubj')
        attr = next(TNode(c.head, {'functor':Functor.ATTR}, [])
                for c in tnode.children if c.function['fun'] != 'ncsubj')
        return TNode(subj.head, tnode.function, [attr]+subj.children)
    except StopIteration:
        return tnode

extract_copula = TRule(
    match=lambda t: 'lemma' in t.head and t.head['lemma']=='be' and t.function!='aux',
    transform=copula_transform)


def adjective_transform (tnode):
    return TNode(head={'concept':tnode.head['lemma'],'sempos':'J'},
        function=tnode.function,
        children=[])

extract_adjectives = TRule(
    match=lambda t: match_tagclass(t, 'J'),
    transform=adjective_transform)


def preposition_transform (tnode):
    try:
        obj = next(c for c in tnode.children if c.function['fun']=='dobj')
        return TNode(head=obj.head,
            function={'functor':True,'fun':'PREP','pval':tnode.head['lemma']},
            children=obj.children)
    except StopIteration:
        return tnode

preposition_rising = TRule(
    match=lambda t: 'tag' in t.head and t.head['tag'] == 'IN',
    transform=preposition_transform)


def juxtapose_link (a, b):
    return (Functor.JUX, {})

grammar = IRG(
    transform_rules = [
        extract_nouns,
        extract_copula,
        extract_pverbs,
        extract_adjectives,
        preposition_rising
    ],
    link_rules = [
        juxtapose_link
    ])
