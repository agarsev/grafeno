from conceptgraphs import Functor
from collections import deque

def linearize (cg):
    g = cg._g
    roots = deque()
    for n in g.nodes():
        if g.node[n]['gram']['sempos'] == 'V':
            roots.append(n)
            break
    processed = set()
    out = ''
    while len(roots)>0:
        node = roots.popleft()
        processed.add(node)
        data = g.node[node]
        if data['gram']['sempos'] == 'V':
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
        elif data['gram']['sempos'] == 'N':
            for n in g[node]:
                ftor = g[node][n]['functor']
                if ftor == Functor.ATTR:
                    out += 'is('+data['concept']+','+g.node[n]['concept']+')\n'
        for n in g[node]:
            if g[node][n]['functor'] == Functor.JUX and n not in processed:
                roots.append(n)
    return out
