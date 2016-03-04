def linearize_rec (tree, node):
    data = tree.node[node]
    if data['type'] == 'V':
        subj = None
        verb = data['concept']
        dobj = None
        comps = []
        for n in tree[node]:
            edge = tree[node][n]['type']
            if edge == 'AGENT':
                subj = linearize_rec(tree, n)
            elif edge == 'THEME':
                dobj = linearize_rec(tree, n)
            else:
                cc = linearize_rec(tree, n)
                if cc != None:
                    comps.append(edge+' '+cc)
        return ' '.join(w for w in [subj, verb, dobj] + comps if w != None)
    elif data['type'] == 'N':
        return data['concept']+'s'

def linearize (tree):
    return linearize_rec(tree, 0)
