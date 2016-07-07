import itertools as it

from grafeno.graph import Graph as CG

def concept_equal (a, b):
    if a['concept'] == b['concept']:
        return a

def functor_equal (a, b):
    if a['functor'] == b['functor']:
        return a

def _generalize_rec (G, a, b, an, bn, node_generalize, edge_generalize):
    na = a.node[an]
    nb = b.node[bn]
    com = node_generalize (na, nb)
    if com == None:
        return None
    node = G.add_node(**com)
    edgas = a._g[an]
    edgbs = b._g[bn]
    for i, j in it.product(edgas, edgbs):
        e = edge_generalize(edgas[i], edgbs[j])
        if e == None:
            continue
        d = _generalize_rec(G, a, b, i, j, node_generalize, edge_generalize)
        if d != None:
            G.add_edge(node, d, **e)
    return node

def generalize (a, b, node_generalize=concept_equal, edge_generalize=functor_equal):
    '''Take two concept graphs and return a new one which generalizes them'''
    gen = CG()
    aroot = [n['id'] for n in a.nodes() if n['sempos'] == 'v'][0]
    broot = [n['id'] for n in b.nodes() if n['sempos'] == 'v'][0]
    _generalize_rec(gen, a, b, aroot, broot, node_generalize, edge_generalize)
    return gen
