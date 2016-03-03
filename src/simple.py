def simple_rule (head, function, children):
    if 'tag' in head and head['tag'][0] == 'N':
        deps = [ (c, 'ATTR', ds) for c, fun, ds in children if c and fun == 'ncmod' ]
        return ({'concept':head['lemma'],'type':'N'},function,deps)
    elif 'tag' in head and head['tag'][0] == 'V':
        deps = []
        for c, fun, ds in children:
            if fun == 'ncsubj':
                deps.append((c, 'AGENT', ds))
            elif fun == 'dobj':
                deps.append((c, 'THEME', ds))
        return ({'concept':head['lemma'],'type':'V'},function,deps)

rules = [ simple_rule ]
