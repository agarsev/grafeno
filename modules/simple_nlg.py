from conceptgraphs import Functor

def linearize_rec (tree, node):
    data = tree.node[node]
    if data['gram']['sempos'] == 'V':
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
    elif data['gram']['sempos'] == 'N':
        return data['concept']+'s'

def linearize (tree):
    return linearize_rec(tree, 0)
