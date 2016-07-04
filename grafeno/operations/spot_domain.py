from collections import deque
import networkx as nx

from grafeno import Graph as CG

def spot_domain (cgraph):

    g = nx.Graph(cgraph._g)
    main = max(g.nodes(), key=lambda n: len(g[n]))

    bunch = set()
    to_process = deque([main])
    while True:
        try:
            n = to_process.popleft()
        except IndexError:
            break
        bunch.add(n)
        for m in g[n]:
            if m not in bunch:
                to_process.append(m)

    return bunch, main

def operate (graph, **args):
    subgraph, main_entity = spot_domain(graph)
    r = CG(graph, subgraph=subgraph)
    r.gram['main_entity'] = main_entity
    return r
