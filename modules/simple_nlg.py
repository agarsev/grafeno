from collections import deque

def linearize_rec (tree, node):
    data = tree.node[node]
    gram = data['gram']
    if gram['sempos'] == 'v':
        subj = None
        verb = data['concept']
        dobj = None
        comps = []
        for n in tree[node]:
            ftor = tree[node][n]['functor']
            if ftor == 'AGENT':
                subj = linearize_rec(tree, n)
            elif ftor == 'THEME':
                dobj = linearize_rec(tree, n)
            elif ftor == 'COMP':
                cc = linearize_rec(tree, n)
                if cc != None:
                    comps.append(tree[node][n]['gram']['pval']+' '+cc)
        return ' '.join(w for w in [subj, verb, dobj] + comps if w != None)
    elif gram['sempos'] == 'n':
        comps = []
        for n in tree[node]:
            ftor = tree[node][n]['functor']
            if ftor == 'ATTR':
                comps.append(linearize_rec(tree, n))
        word = data['concept']
        if gram.get('num') == 'p':
            word += 's'
        return ' '.join(comps + [word])
    elif gram['sempos'] == 'j':
        return data['concept']

def linearize (cgraph):
    g = cgraph._g
    sentences = deque()
    for n in g.nodes():
        if g.node[n]['gram']['sempos'] == 'v':
            sentences.append(n)
    results = []
    processed = set()
    while len(sentences)>0:
        n = sentences.popleft()
        processed.add(n)
        s = linearize_rec(g, n)
        if s:
            s = s.replace('_',' ')
            results.append(s[0].upper() + s[1:] + '.')
    return ' '.join(results)
