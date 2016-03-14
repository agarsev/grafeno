from conceptgraphs import Functor
from collections import deque

def linearize (g):
    roots = deque([0])
    out = ''
    while len(roots)>0:
        node = roots.popleft()
        data = g.node[node]
        if data['gram']['type'] == 'V':
            subj = None
            verb = data['concept']
            dobj = None
            for n in g[node]:
                ftor = g[node][n]['functor']
                if ftor == Functor.AGENT:
                    subj = g.node[n]['concept']
                elif ftor == Functor.THEME:
                    dobj = g.node[n]['concept']
            if subj and dobj:
                out += verb+'('+subj+','+dobj+')\n'
        elif data['gram']['type'] == 'N':
            for n in g[node]:
                ftor = g[node][n]['functor']
                if ftor == Functor.ATTR:
                    out += 'is('+data['concept']+','+g.node[n]['concept']+')\n'
        for n in g[node]:
            if g[node][n]['functor'] == Functor.JUX:
                roots.append(n)
    return out
