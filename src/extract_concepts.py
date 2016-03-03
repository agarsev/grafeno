#!/usr/bin/env python3

import json
import networkx as nx

def transform_node (tree, node, function, rules):
    '''Take a dependency node and process it according to the rules'''
    children = []
    if 'children' in node:
        for c in node['children']:
            concept = transform_node(tree, c, c["function"], rules)
            if concept != None:
                children.append(concept)
    head = tree['tokenmap'][node['token']].copy()
    for r in rules:
        match = r(head, function, children)
        if match == None:
            continue
        else:
            head, function, children = match
    if 'concept' not in head:
        return None
    return (head, function, children)

graph_id = 0
def tree_to_graph (G, tree):
    global graph_id
    head, function, children = tree
    pid = graph_id
    graph_id += 1
    G.add_node(pid, concept=head['concept'], type=head['type'])
    for c in children:
        G.add_edge(pid, tree_to_graph(G, c), type=c[1])
    return pid

def transform_tree (tree, rules_module = 'transform'):
    T = __import__(rules_module)
    global graph_id
    '''Take a dependency tree extracted from Freeling and extract the conceptual graph'''
    tree['tokenmap'] = { t['id']: t for t in tree['tokens'] }
    res = transform_node(tree, tree['dependencies'][0], 'top', T.rules)
    if res == None:
        return None
    graph_id = 0
    G = nx.DiGraph()
    tree_to_graph(G, res)
    return G


if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description='Extract the conceptual graph of a document')
    arg_parser.add_argument('doc', help='document')
    arg_parser.add_argument('-p','--plot',action='store_true',help="Show a plot of the graph instead of dumping it")
    arg_parser.add_argument('-t','--transform',help="Transformer module to use",default='transform')
    args = arg_parser.parse_args()

    with open(args.doc, mode='r') as f:
        trees = json.load(f)

    for t in trees:
        g = transform_tree(t, args.transform)
        if g == None:
            continue
        if args.plot:
            from common import draw_concept_graph
            draw_concept_graph(g)
        else:
            from networkx.readwrite import json_graph
            print(json.dumps(json_graph.node_link_data(g)))
