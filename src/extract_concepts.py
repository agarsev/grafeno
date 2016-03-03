#!/usr/bin/env python3

import json
import networkx as nx

def extract_nouns (head, function, children):
    if 'tag' in head and head['tag'][0] == 'N':
        deps = [ (c, 'ATTR', ds) for c, fun, ds in children if c and fun == 'ncmod' ]
        return ({'concept':head['lemma'],'type':'N'},function,deps)

def predicative_verbs (head, function, children):
    if 'tag' in head and head['tag'][0] == 'V' and function != 'aux':
        deps = []
        for c, fun, ds in children:
            if fun == 'ncsubj':
                deps.append((c, 'AGENT', ds))
            elif fun == 'dobj':
                deps.append((c, 'THEME', ds))
            elif fun == 'PREP':
                deps.append((c, c['prep'], ds))
        return ({'concept':head['lemma'],'type':'V'},function,deps)

def copula (head, function, children):
    if 'lemma' in head and head['lemma'] == 'be' and function != 'aux':
        try:
            subj = next((c, ds) for c, fun, ds in children if fun == 'ncsubj')
            attr = next((c, 'ATTR', []) for c, fun, ds in children if fun == 'ncmod')
            return (subj[0], function, [attr]+subj[1])
        except StopIteration:
            pass

def extract_adjectives (head, function, children):
    if 'tag' in head and head['tag'][0] == 'J':
        return ({'concept':head['lemma'],'type':'J'},function,[])

def preposition_rising (head, function, children):
    if 'tag' in head and head['tag'] == 'IN':
        try:
            obj = next((c, ds) for c, fun, ds in children if fun == 'dobj')
            obj[0]['prep'] = head['lemma']
            return (obj[0], 'PREP', obj[1])
        except StopIteration:
            pass

rules = [ extract_nouns, copula, predicative_verbs, extract_adjectives, preposition_rising ]

def transform_node (tree, node, function):
    '''Take a dependency node and process it according to the rules'''
    children = []
    if 'children' in node:
        for c in node['children']:
            concept = transform_node(tree, c, c["function"])
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

def transform_tree (tree):
    global graph_id
    '''Take a dependency tree extracted from Freeling and extract the conceptual graph'''
    tree['tokenmap'] = { t['id']: t for t in tree['tokens'] }
    res = transform_node(tree, tree['dependencies'][0], 'top')
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
    args = arg_parser.parse_args()

    with open(args.doc, mode='r') as f:
        trees = json.load(f)

    for t in trees:
        g = transform_tree(t)
        if g == None:
            continue
        if args.plot:
            import matplotlib.pyplot as plt
            lay = nx.spring_layout(g)
            nx.draw_networkx(g,lay,node_size=1000,node_color="white", labels={n:data['concept'] for n, data in g.nodes(True)})
            nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['type'] for (a,b,data) in g.edges(data=True)})
            plt.show()
        else:
            from networkx.readwrite import json_graph
            print(json.dumps(json_graph.node_link_data(g)))
