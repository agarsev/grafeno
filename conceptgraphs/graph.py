import json
import networkx as nx
from networkx.readwrite import json_graph

from .freeling_parse import parse, extract_semgraph

class Graph:

    def __init__ (self, use_freeling=False, transformer=None, transformer_args={}, text=None):
        self.node_id = 0
        self._g = nx.DiGraph()
        self.gram = {}
        if use_freeling:
            self.use_freeling = True
            self.transformer = None
        elif transformer:
            self.use_freeling = False
            self.transformer = transformer(graph=self, **transformer_args)
        else:
            raise ValueError('Either a transformer or using freeling is required')
        if text:
            self.add_text(text)

    def add_node (self, concept, gram={}):
        nid = self.node_id
        self.node_id += 1
        self._g.add_node(nid, id=nid, concept=concept, gram=gram)
        return nid

    def add_edge (self, head, dependent, functor, gram={}):
        if head not in self._g or dependent not in self._g:
            raise ValueError('Head or dependent are not in the graph ('+str(functor)+')')
        self._g.add_edge(head, dependent, functor=functor, gram=gram)

    def add_text (self, text):
        result = parse(text, self.use_freeling)
        if self.use_freeling:
            extract_semgraph(result, self)
        else:
            for s in result:
                t = self.transformer.transform_sentence(s)

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
        ret = Graph(use_freeling=self.use_freeling,transformer=self.transformer)
        ret.node_id = self.node_id
        ret.gram = self.gram
        if keep:
            ret._g = nx.DiGraph(self._g.subgraph(n for n in self._g.nodes()
                        if keep(self._g.node[n])))
        else:
            ret._g = nx.DiGraph(self._g)
        return ret

    def to_json (self, with_labels = True):
        class SkipEncoder(json.JSONEncoder):
            def default(self, obj):
                return None
        g = self._g
        if with_labels:
            for n in g:
                g.node[n]['label'] = g.node[n]['concept']
                for m in g[n]:
                    g[n][m]['label'] = g[n][m]['functor']
        return json.dumps(json_graph.node_link_data(g), cls=SkipEncoder)
