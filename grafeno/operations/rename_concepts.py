def operate (graph, **args):
    for n in graph.nodes():
        if 'negative' in n:
            n['concept'] = 'not_'+n['concept']
    return graph
