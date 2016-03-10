from enum import Enum
import networkx as nx

from .tree_transform import transform_tree
from .freeling_parse import parse

class Functor(Enum):

    AGENT = 1
    THEME = 2
    ADV = 3
    ATTR = 4
    JUX = 5

    def is_semantic(self):
        return self.value in {1, 2, 3, 4}

    def is_discourse(self):
        return self.value in {5,}

class Graph:

    def __init__ (self, rules=[], text=None):
        self.node_id = 0
        self._g = nx.DiGraph()
        self.rules = rules
        self.last_sentence = None
        if text:
            self.add_text(text)

    def add_node (self, concept, gram=None):
        nid = self.node_id
        self.node_id += 1
        self._g.add_node(nid, concept=concept, gram=gram)
        return nid

    def add_edge (self, head, dependent, functor, gram=None):
        self._g.add_edge(head, dependent, functor=functor, gram=gram)

    def __add_node_recursive (self, tree):
        head, function, children = tree
        nid = self.add_node(head['concept'], head)
        for c in children:
            self.add_edge(nid, self.__add_node_recursive(c), c[1]['functor'], c[1])
        return nid

    def __link (self, fro, to):
        self.add_edge(fro, to, Functor.JUX)

    def add_text (self, text):
        parses = parse(text)
        for p in parses:
            t = transform_tree(p, self.rules)
            nunode = self.__add_node_recursive(t)
            if self.last_sentence != None:
                self.__link(self.last_sentence, nunode)
            self.last_sentence = nunode

    def add_html (self, html):
        from .html_to_text import html_to_text
        self.add_text(html_to_text(html))

    def draw (self):
        import matplotlib.pyplot as plt
        g = self._g
        lay = nx.spring_layout(g)
        nx.draw_networkx_nodes(g,lay,node_size=3000,node_color="white",linewidths=0)
        nx.draw_networkx_labels(g,lay,labels={n:data['concept'] for n, data in g.nodes(True)})
        nx.draw_networkx_edges(g,lay)
        nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['functor'] for (a,b,data) in g.edges(data=True)})
        plt.show()
