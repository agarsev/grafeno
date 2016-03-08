from conceptgraphs import Functor

# NODEs are 3-tuples of:
# - head: dictionary. Syntactic features and already processed
#       grammatemes. `concept` should have the tectogrammatical lemma.
#       If no concept is found in the end, the node is dropped.
# - function: dictionary. In `fun` is the syntactic dependency, in
#       `ftor` should be the Functor. Other attributes are grammatemes
#       of the dependency.
#       If no ftor is found in the end, the edge and children are dropped.
# string or Functor. Either the syntactic dependency
#       or the already processed Functor
# - children: list of NODEs (3-tuples)
#
# Each rule should take a 3-tuple and return a 3-tuple partially processed,
# or return None to indicate no processing happened

def extract_nouns (head, function, children):
    if 'tag' in head and head['tag'][0] == 'N':
        deps = []
        for c, f, ds in children:
            if c and f['fun'] == 'ncmod':
                deps.append((c, {'ftor': Functor.ATTR}, ds))
        return ({'concept':head['lemma'],'type':'N'},function,deps)

def predicative_verbs (head, function, children):
    if 'tag' in head and head['tag'][0] == 'V' and function != 'aux':
        deps = []
        for c, fun, ds in children:
            f = {}
            synt = fun['fun']
            if synt == 'ncsubj':
                f['ftor'] = Functor.AGENT
            elif synt == 'dobj':
                f['ftor'] = Functor.THEME
            elif synt == 'PREP':
                f['ftor'] = Functor.ADV
                f['pval'] = fun['pval']
            deps.append((c, f, ds))
        return ({'concept':head['lemma'],'type':'V'},function,deps)

def copula (head, function, children):
    if 'lemma' in head and head['lemma'] == 'be' and function != 'aux':
        try:
            subj = next((c, ds) for c, fun, ds in children if fun == 'ncsubj')
            attr = next((c, {'ftor':Funcor.ATTR}, []) for c, fun, ds in children if fun == 'ncmod')
            return (subj[0], function, [attr]+subj[1])
        except StopIteration:
            pass

def extract_adjectives (head, function, children):
    if 'tag' in head and head['tag'][0] == 'J':
        return ({'concept':head['lemma'],'type':'J'},function,[])

def preposition_rising (head, function, children):
    if 'tag' in head and head['tag'] == 'IN':
        try:
            obj = next((c, ds) for c, f, ds in children if f['fun'] == 'dobj')
            return (obj[0], {'fun':'PREP','pval':head['lemma']}, obj[1])
        except StopIteration:
            pass

rules = [ extract_nouns, copula, predicative_verbs, extract_adjectives, preposition_rising ]
