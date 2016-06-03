def filter_edges (cgraph, remove=[]):
    g = cgraph._g
    to_rem = [(n,m) for n in g for m in g[n] if g[n][m]['functor'] in remove]
    g.remove_edges_from(to_rem)

