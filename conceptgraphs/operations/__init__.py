from .clustering2 import cluster

def operate (graph, operation, **args):

    if operation == 'cluster':
        HVS, clusters = cluster(graph, **args)
        graph.gram['HVS'] = HVS
        graph.gram['clusters'] = clusters
        return graph

    raise ValueError("Unknown operation")
