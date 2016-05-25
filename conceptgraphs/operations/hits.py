from collections import defaultdict
import math

def hits (graph, epsilon = 1e-5, max_its = 100):

    auth = defaultdict(lambda:1)
    hub = defaultdict(lambda:1)

    g = graph._g
    weight = { (a,b): data['gram'].get('weight', 1)
            for a, b, data in g.edges_iter(data=True) }

    delta = epsilon+1
    its = 0
    prev_total = 0

    while delta > epsilon and its < max_its:

        for a, b in g.edges_iter():
            auth[b] += weight[(a,b)] * hub[a]
        for a, b in g.edges_iter():
            hub[a] += weight[(a,b)] * auth[b]

        totauth = math.sqrt(sum(auth[n]**2 for n in g.nodes()))
        tothub = math.sqrt(sum(hub[n]**2 for n in g.nodes()))

        for n in g.nodes():
            auth[n] /= totauth
            hub[n] /= tothub

        delta = abs(totauth + tothub - prev_total)
        prev_total = totauth + tothub
        its += 1

    auth.default_factory = lambda:0
    hub.default_factory = lambda:0
    return auth, hub
