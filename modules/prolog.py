from collections import deque

def valid (node):
    return node['gram']['sempos'] in {'n','v'}

class Linearizer:

    def __init__ (self, graph=None, **kwds):
        self.graph = graph
        me = max(graph._g.nodes(), key=lambda n: len(graph._g[n]))
        self.main_entity = self.graph._g.node[me]['concept']

    def get_starter_nodes (self):
        ns = self.graph._g.node
        return [n for n in ns if valid(ns[n])]

    def process_node (self, node, edges):
        g = self.graph._g
        me = self.main_entity
        rels = ["r("+','.join([me, node['concept'], edges[m]['functor'], g.node[m]['concept']])+")." for m in edges]
        text = '\n'.join(rels) if len(rels)>0 else ''
        self.waiting += [m for m in edges if valid(g.node[m])]
        return text

    def linearize (self):
        g = self.graph._g
        self.waiting = deque(self.get_starter_nodes())
        w = self.waiting
        processed = set()
        results = [':- multifile r/4, neg/4, arc/5, rule/6, frame/6, integrity/3.\n']
        while len(w)>0:
            n = w.popleft()
            if n in processed:
                continue
            processed.add(n)
            text = self.process_node(g.node[n], g[n])
            if text:
                results.append(text)
        return '\n'.join(results)
