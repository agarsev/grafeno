from collections import deque

def linearize (cg):
    g = cg._g
    roots = deque()
    for n in g.nodes():
        if g.node[n]['gram']['sempos'] in {'v','n'}:
            roots.append(n)
    processed = set()
    out = ''
    while len(roots)>0:
        node = roots.popleft()
        processed.add(node)
        data = g.node[node]
        if data['gram']['sempos'] == 'v':
            subj = None
            verb = data['concept']
            dobj = None
            for n in g[node]:
                ftor = g[node][n]['functor']
                if ftor == 'AGENT':
                    subj = g.node[n]['concept']
                elif ftor == 'THEME':
                    dobj = g.node[n]['concept']
            if subj and dobj:
                out += verb+'('+subj+','+dobj+')\n'
        elif data['gram']['sempos'] == 'n':
            for n in g[node]:
                ftor = g[node][n]['functor']
                if ftor == 'ATTR':
                    out += 'is('+data['concept']+','+g.node[n]['concept']+')\n'
    return out
