from collections import deque

def valid (node):
    return node['gram']['sempos'] in {'v',}

class Linearizer:

    def __init__ (self, graph=None, **kwds):
        self.graph = graph

    def get_starter_nodes (self):
        ns = self.graph._g.node
        return [n for n in ns if valid(ns[n])]

    def process_node (self, node, edges):
        g = self.graph._g
        gram = node['gram']
        if gram['sempos'] == 'v':
            subj = None
            verb = node['concept']
            dobj = None
            comps = []
            for n in edges:
                ftor = edges[n]['functor']
                if ftor == 'AGENT':
                    subj = self.process_node(g.node[n], g[n])
                elif ftor == 'THEME':
                    dobj = self.process_node(g.node[n], g[n])
                elif ftor == 'COMP':
                    cc = self.process_node(g.node[n], g[n])
                    if cc != None:
                        comps.append(edges[n]['gram']['pval']+' '+cc)
            return ' '.join(w for w in [subj, verb, dobj] + comps if w != None)
        elif gram['sempos'] == 'n':
            comps = []
            for n in edges:
                ftor = edges[n]['functor']
                if ftor == 'ATTR':
                    comps.append(self.process_node(g.node[n], g[n]))
            word = node['concept']
            if gram.get('num') == 'p':
                word += 's'
            return ' '.join(comps + [word])
        elif gram['sempos'] == 'j':
            return node['concept']

    def linearize (self):
        g = self.graph._g
        self.waiting = deque(self.get_starter_nodes())
        w = self.waiting
        processed = set()
        results = []
        while len(w)>0:
            n = w.popleft()
            if n in processed:
                continue
            processed.add(n)
            text = self.process_node(g.node[n], g[n])
            if text:
                s = text.replace('_',' ')
                results.append(s[0].upper()+s[1:]+'.')
        return ' '.join(results)
