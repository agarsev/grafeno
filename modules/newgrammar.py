from conceptgraphs.grammar import NodeRule, EdgeRule, TGrammar

class Nouns (NodeRule):

    def match (self, msnode):
        return msnode.get('pos') == 'noun'

    def transform (self, msnode, semnode):
        semnode['concept'] = msnode.get('lemma')
        semnode['sempos'] = 'n'
        semnode['proper'] = msnode.get('type') == 'proper'
        semnode['num'] = msnode.get('num','p')

class Adjectives (NodeRule):

    def match (self, msnode):
        return msnode.get('pos') == 'adjective'

    def transform (self, msnode, semnode):
        semnode['concept'] = msnode.get('lemma')
        semnode['sempos'] = 'j'

class Verbs (NodeRule):

    def match (self, msnode):
        return msnode.get('pos') == 'verb'

    def transform (self, msnode, semnode):
        semnode['concept'] = msnode.get('lemma')
        semnode['sempos'] = 'v'
        semnode['tense'] = msnode.get('vform')

class Predication (EdgeRule):

    def match (self, dep, head, child):
        return dep in {'ncsubj','dobj','iobj'} and head.get('sempos')=='v'

    def transform (self, dep, head, child):
        if dep == 'ncsubj':
            return ('AGENT', head['id'], child['id'], {})
        elif dep == 'dobj':
            return ('THEME', head['id'], child['id'], {})
        elif dep == 'iobj':
            return ('IOBJ', head['id'], child['id'], {})

class Attribution (EdgeRule):

    def match (self, dep, head, child):
        return dep == 'ncmod'

    def transform (self, dep, head, child):
        return ('ATTR', head['id'], child['id'], {})

class Grammar (TGrammar):

    def __init__ (self):
        super().__init__(
            node_transforms = [ Nouns, Adjectives, Verbs ],
            edge_transforms = [ Predication, Attribution ]
            )
