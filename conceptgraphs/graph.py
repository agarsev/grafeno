import networkx as nx

from .tree_transform import transform_tree
from .freeling_parse import parse

class graph:

    def __init__ (self, rules, text=None):
        self.node_id = 0
        self.g = nx.DiGraph()
        self.rules = rules
        if text:
            self.add_text(text)

    def __add_node_recursive (self, tree):
        head, function, children = tree
        nid = self.node_id
        self.node_id += 1
        self.g.add_node(nid, concept=head['concept'], type=head['type'])
        for c in children:
            self.g.add_edge(nid, self.__add_node_recursive(c), type=c[1])
        return nid

    def add_text (self, text):
        t = transform_tree(parse(text), self.rules)
        self.__add_node_recursive(t)

    def add_html (self, html):
        from .html_to_text import html_to_text
        self.add_text(html_to_text(html))

    def draw (self):
        import matplotlib.pyplot as plt
        g = self.g
        lay = nx.spring_layout(g)
        nx.draw_networkx_nodes(g,lay,node_size=3000,node_color="white",linewidths=0)
        nx.draw_networkx_labels(g,lay,labels={n:data['concept'] for n, data in g.nodes(True)})
        nx.draw_networkx_edges(g,lay)
        nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['type'] for (a,b,data) in g.edges(data=True)})
        plt.show()
