from collections import deque

from conceptgraphs import Functor

def linearize_rec (tree, node):
    data = tree.node[node]
    gram = data['gram']
    if gram['sempos'] == 'V':
        subj = None
        verb = data['concept']
        dobj = None
        comps = []
        for n in tree[node]:
            ftor = tree[node][n]['functor']
            if ftor == Functor.AGENT:
                subj = linearize_rec(tree, n)
            elif ftor == Functor.THEME:
                dobj = linearize_rec(tree, n)
            elif ftor == Functor.COMP:
                cc = linearize_rec(tree, n)
                if cc != None:
                    comps.append(tree[node][n]['gram']['pval']+' '+cc)
        return ' '.join(w for w in [subj, verb, dobj] + comps if w != None)
    elif gram['sempos'] == 'N':
        comps = []
        for n in tree[node]:
            ftor = tree[node][n]['functor']
            if ftor == Functor.ATTR:
                comps.append(linearize_rec(tree, n))
        word = data['concept']
        if 'number' in gram and gram['number'] == 'plural':
            word += 's'
        return ' '.join(comps + [word])
    elif gram['sempos'] == 'J':
        return data['concept']

def linearize (cgraph):
    g = cgraph._g
    sentences = deque()
    for n in g.nodes():
        if g.node[n]['gram']['sempos'] == 'V':
            sentences.append(n)
            break
    results = []
    while len(sentences)>0:
        n = sentences.popleft()
        for m in g[n]:
            ftor = g[n][m]['functor']
            if ftor == Functor.JUX:
                sentences.append(m)
        s = linearize_rec(g, n)
        if s:
            s = s.replace('_',' ')
            results.append(s[0].upper() + s[1:] + '.')
    return ' '.join(results)
