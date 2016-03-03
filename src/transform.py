def extract_nouns (head, function, children):
    if 'tag' in head and head['tag'][0] == 'N':
        deps = [ (c, 'ATTR', ds) for c, fun, ds in children if c and fun == 'ncmod' ]
        return ({'concept':head['lemma'],'type':'N'},function,deps)

def predicative_verbs (head, function, children):
    if 'tag' in head and head['tag'][0] == 'V' and function != 'aux':
        deps = []
        for c, fun, ds in children:
            if fun == 'ncsubj':
                deps.append((c, 'AGENT', ds))
            elif fun == 'dobj':
                deps.append((c, 'THEME', ds))
            elif fun == 'PREP':
                deps.append((c, c['prep'], ds))
        return ({'concept':head['lemma'],'type':'V'},function,deps)

def copula (head, function, children):
    if 'lemma' in head and head['lemma'] == 'be' and function != 'aux':
        try:
            subj = next((c, ds) for c, fun, ds in children if fun == 'ncsubj')
            attr = next((c, 'ATTR', []) for c, fun, ds in children if fun == 'ncmod')
            return (subj[0], function, [attr]+subj[1])
        except StopIteration:
            pass

def extract_adjectives (head, function, children):
    if 'tag' in head and head['tag'][0] == 'J':
        return ({'concept':head['lemma'],'type':'J'},function,[])

def preposition_rising (head, function, children):
    if 'tag' in head and head['tag'] == 'IN':
        try:
            obj = next((c, ds) for c, fun, ds in children if fun == 'dobj')
            obj[0]['prep'] = head['lemma']
            return (obj[0], 'PREP', obj[1])
        except StopIteration:
            pass

rules = [ extract_nouns, copula, predicative_verbs, extract_adjectives, preposition_rising ]
