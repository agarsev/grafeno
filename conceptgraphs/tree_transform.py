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
    func = { 'fun': function }
    for r in rules:
        match = r(head, func, children)
        if match == None:
            continue
        else:
            head, function, children = match
    if 'concept' not in head:
        return None
    children = [c for c in children if 'ftor' in c[1]]
    return (head, function, children)


def transform_tree (tree, rules):
    '''Take a dependency tree extracted from Freeling and extract the conceptual graph'''
    tree['tokenmap'] = { t['id']: t for t in tree['tokens'] }
    return transform_node(tree, tree['dependencies'][0], 'top', rules)

