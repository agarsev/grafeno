from itertools import combinations
import networkx as nx

def cluster (cgraph, hubratio = 0.2):
    g = nx.Graph(cgraph._g)

    def weight (n, m):
        return g[n][m].get('weight',1)

    def intra_con (a):
        return sum(weight(n, m) for n, m in combinations(a, 2) if m in g[n])

    def inter_con (a, b):
        return sum(weight(n, m) for n in a for m in b if m in g[n])

    saliences = sorted(g.nodes(), reverse=True, \
            key=lambda n: sum(weight(n, m) for m in g[n]))

    hubnumber = int(len(g.nodes())*hubratio)
    hub_v = saliences[:hubnumber]
    nonhub_v = saliences[hubnumber:]

    # Make HVS from sets of highly connected hub vertices
    preHVS = { n:[n] for n in hub_v }
    for n in hub_v:
        maximal = max(hub_v, key=lambda m: inter_con([n],[m]) if m != n else 1e-10)
        if maximal != n:
            preHVS[maximal] += preHVS[n]
            preHVS[n] = []
    HVS = [preHVS[h] for h in preHVS if len(preHVS[h])>0]

    # Merge HVS more interconnected
    change = True
    while change:
        change = False
        for a, b in combinations(HVS, 2):
            inter = inter_con(a, b)
            intra = max(intra_con(a), intra_con(b))
            if inter > intra:
                change = True
                a += b
                b = []
                break
        HVS = [h for h in HVS if len(h)>0]

    # HVS of length 1 don't deserve to be hub
    demoted = [h[0] for h in HVS if len(h)==1]
    nonhub_v = demoted + nonhub_v
    HVS = [h for h in HVS if len(h)>1]
    if len(HVS)<1:
        return [[nonhub_v[0]]], [nonhub_v]

    # Assign non-hub vertices to HVS
    # TODO: check whether select max instead of going forward
    # Note that forward might make sense because they are ordered according to salience
    clusters = [h.copy() for h in HVS]
    for n in nonhub_v:
        best = max(clusters, key=lambda h: inter_con([n],h))
        best.append(n)

    return HVS, clusters

def operate (graph, **args):
    HVS, clusters = cluster(graph, **args)
    graph.gram['HVS'] = HVS
    graph.gram['clusters'] = clusters
    return graph
