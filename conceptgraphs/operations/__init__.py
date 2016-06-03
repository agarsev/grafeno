from conceptgraphs import Graph as CG

from .clustering2 import cluster
from .spot_domain import spot_domain
from .filters import filter_edges

def operate (graph, operation, **args):

    if operation == 'cluster':
        HVS, clusters = cluster(graph, **args)
        graph.gram['HVS'] = HVS
        graph.gram['clusters'] = clusters
        return graph

    if operation == 'spot_domain':
        subgraph, main_entity = spot_domain(graph, **args)
        r = CG(graph, subgraph=subgraph)
        r.gram['main_entity'] = main_entity
        return r

    if operation == 'filter_edges':
        filter_edges(graph, **args)
        return graph

    raise ValueError("Unknown operation")
