# By Alberto Fernández Isabel
# Requires python-louvain
import networkx as nx
from optional_import import optional_import

with optional_import():
    import community

def cluster (graph):
    g = nx.Graph(graph._g)
    for n in g.node:
        g.node[n] = {}
    part = community.best_partition(g)
    clusters = [[] for v in set(part.values())]
    for n in part.keys():
        clusters[part[n]].append(n)
    return clusters
