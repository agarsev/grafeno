from collections import defaultdict
import math

def hits (graph, epsilon = 1e-5, max_its = 100):
    auth = defaultdict(lambda:1)
    hub = defaultdict(lambda:1)
    g = graph._g
    delta = epsilon+1
    its = 0
    while delta > epsilon and its < max_its:
        prev_auth = auth
        prev_hub = hub
        auth = defaultdict(lambda:0)
        hub = defaultdict(lambda:0)
        for a, b, data in g.edges_iter(data=True):
            gram = data['gram']
            weight = gram['weight'] if 'weight' in gram else 1
            auth[b] += weight * prev_hub[a]
            hub[a] += weight * prev_auth[b]
        for n in g.nodes():
            sum = math.sqrt(auth[n]**2+hub[n]**2)
            if sum>0:
                auth[n] /= sum
                hub[n] /= sum
        delta = 0
        for n in g.nodes():
            delta += abs(auth[n] - prev_auth[n])
            delta += abs(hub[n] - prev_hub[n])
        delta /= 2*len(g.nodes())
        its += 1
    return auth, hub
