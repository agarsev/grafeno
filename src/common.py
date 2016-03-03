import networkx as nx
import matplotlib.pyplot as plt

def draw_concept_graph (g):
    lay = nx.spring_layout(g)
    nx.draw_networkx_nodes(g,lay,node_size=3000,node_color="white",linewidths=0)
    nx.draw_networkx_labels(g,lay,labels={n:data['concept'] for n, data in g.nodes(True)})
    nx.draw_networkx_edges(g,lay)
    nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['type'] for (a,b,data) in g.edges(data=True)})
    plt.show()
