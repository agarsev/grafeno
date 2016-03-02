#!/usr/bin/env python3

import json
import networkx as nx

def simplerule (head, children):
    if head['tag'][0] == 'N':
        return ({'concept':head['lemma'],'type':'N'},[])
    elif head['tag'][0] == 'V':
        deps = [ (c, 'ARG') for c, fun in children if c and fun in ("ncsubj","ncmod","dobj") ]
        return ({'concept':head['lemma'],'type':'V'},deps)
    return (None, None)

rules = [ simplerule ]

graph_id = 0

def transform_node (G, tree, node):
    '''Take a dependency node and process it according to the rules'''
    global graph_id
    for r in rules:
        if 'children' in node:
            children = [ (transform_node(G, tree, c), c["function"]) for c in node['children'] ]
        else:
            children = []
        head = tree['tokenmap'][node['token']]
        p, deps = r(head, children)
        if p != None:
            pid = graph_id
            graph_id += 1
            G.add_node(pid, concept=p['concept'], type=p['type'])
            p['id'] = pid
            for d, fun in deps:
                G.add_edge(pid, d['id'], type=fun)
            return p

def transform_tree (tree):
    '''Take a dependency tree extracted from Freeling and extract the conceptual graph'''
    global graph_id
    G = nx.DiGraph()
    graph_id = 0
    tree['tokenmap'] = { t['id']: t for t in tree['tokens'] }
    transform_node(G, tree, tree['dependencies'][0])
    return G


if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Extract the conceptual graph of a document')
    arg_parser.add_argument('doc', help='document')
    arg_parser.add_argument('-p','--plot',action='store_true',help="Show a plot of the graph instead of dumping it")
    args = arg_parser.parse_args()

    with open(args.doc, mode='r') as f:
        tree = json.load(f)

    g = transform_tree(tree[0])

    if args.plot:

        import matplotlib.pyplot as plt
        lay = nx.spring_layout(g)
        nx.draw_networkx(g,lay,node_size=1000,node_color="white", labels={n:data['concept'] for n, data in g.nodes(True)})
        nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['type'] for (a,b,data) in g.edges(data=True)})
        plt.show()

    else:

        from networkx.readwrite import json_graph
        print(json.dumps(json_graph.node_link_data(g)))
