# By Alberto Fernández Isabel
# Requires python-louvain
import networkx as nx
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

def operate (graph, **args):
    clusters = cluster(graph, **args)
    graph.gram['clusters'] = clusters
    return graph
