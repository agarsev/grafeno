from collections import defaultdict

def filter_edges (cgraph, remove=[], rename={}, frequency=None):
    g = cgraph._g
    to_rem = []
    if frequency:
        freqs = defaultdict(lambda:0)
        for n, m, d in g.edges_iter(data=True):
            freqs[d['functor']] += 1
    for n, m, d in g.edges_iter(data=True):
        ftor = d['functor']
        if frequency and (freqs[ftor]>frequency['max'] or freqs[ftor]<frequency['min']):
            to_rem.append((n,m))
        if ftor in rename:
            d['functor'] = rename[ftor]
        if ftor in remove:
            to_rem.append((n,m))
    g.remove_edges_from(to_rem)

def operate (graph, **args):
    filter_edges(graph, **args)
    return graph
