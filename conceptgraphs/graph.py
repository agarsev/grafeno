import networkx as nx

from .freeling_parse import parse

class Graph:

    def __init__ (self, grammar=None, text=None):
        self.node_id = 0
        self._g = nx.DiGraph()
        self.tgrammar = grammar
        if text:
            self.add_text(text)

    def add_node (self, concept, gram={}):
        nid = self.node_id
        self.node_id += 1
        self._g.add_node(nid, id=nid, concept=concept, gram=gram)
        return nid

    def add_edge (self, head, dependent, functor, gram={}):
        self._g.add_edge(head, dependent, functor=functor, gram=gram)

    def add_text (self, text):
        parses = parse(text)
        for p in parses:
            t = self.tgrammar.transform_sentence(p, self)

    def draw (self, bunch=None):
        import matplotlib.pyplot as plt
        if bunch:
            g = self._g.subgraph(bunch)
        else:
            g = self._g
        lay = nx.spring_layout(g)
        nx.draw_networkx_nodes(g,lay,node_size=3000,node_color="white",linewidths=0)
        nx.draw_networkx_labels(g,lay,labels={n:data['concept'] for n, data in g.nodes(True)})
        nx.draw_networkx_edges(g,lay)
        nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['functor'] for (a,b,data) in g.edges(data=True)})
        plt.show()

    def all_concepts (self):
        return set(self._g.node[n]['concept'] for n in self._g.nodes())

    def copy (self, keep=None):
        ret = Graph(grammar=self.tgrammar)
        ret.node_id = self.node_id
        if keep:
            ret._g = nx.DiGraph(self._g.subgraph(n for n in self._g.nodes()
                        if keep(self._g.node[n])))
        else:
            ret._g = nx.DiGraph(self._g)
        return ret
