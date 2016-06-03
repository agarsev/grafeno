def filter_edges (cgraph, remove=[], rename={}):
    g = cgraph._g
    to_rem = []
    for n in g:
        for m in g[n]:
            ftor = g[n][m]['functor']
            if ftor in rename:
                g[n][m]['functor'] = rename[ftor]
            if ftor in remove:
                to_rem.append((n,m))
    g.remove_edges_from(to_rem)

