import networkx as nx

from .freeling_parse import parse

class Graph:

    def __init__ (self, grammar=None, text=None):
        self.node_id = 0
        self._g = nx.DiGraph()
        self.tgrammar = grammar
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

    def __add_node_recursive (self, tnode):
        nid = self.add_node(tnode.head['concept'], tnode.head)
        for c in tnode.children:
            self.add_edge(nid, self.__add_node_recursive(c),
                    c.function['functor'], c.function)
        return nid

    def add_text (self, text):
        parses = parse(text)
        for p in parses:
            t = self.tgrammar.transform_tree(p)
            if t == None:
                continue
            nunode = self.__add_node_recursive(t)
            if self.last_sentence != None:
                fro = self._g.node[self.last_sentence]['gram']
                ftor, gram = self.tgrammar.link_sentences(fro, t)
                if ftor != None:
                    self.add_edge(self.last_sentence, nunode, ftor, gram)
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
