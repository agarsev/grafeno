from collections import deque
from .functor import Functor

class NodeRule:
    '''A rule which partially transforms a morfosyntactic node into a semantic
    one.'''

    def __init__ (self, grammar):
        self.grammar = grammar

    def match (self, msnode):
        '''take a morfosyntactic node (dict) and return whether the rule
        applies to it.'''
        return True

    def transform (self, msnode, semnode):
        '''take a morfosyntactic node (dict) and a semantic node (dict) and
        extend the latter with information from the former. Semantic nodes get
        dropped in the end if they don't have a concept attribute.'''
        pass


class EdgeRule:
    '''A rule which creates a semantic edge according to a dependency
    relation.'''

    def __init__ (self, grammar):
        self.grammar = grammar

    def match (self, dependency, head, child):
        '''take a dependency relation (str) and the parent and child nodes
        (semnodes, dict) and return whether the rule applies to it.'''
        return True

    def transform (self, dependency, head, child):
        '''take a dependency relation (str) and the parent and child nodes
        (semnodes, dict) and return a semantic edge tuple(functor, headid, childid, gram) with the relevant
        information. Semantic edges get dropped in the end if they have an
        empty functor.'''
        return (dependency, head['id'], child['id'], {})


class TGrammar:

    def __init__ (self, node_transforms = [], edge_transforms = []):
        self.nrules = [n(self) for n in node_transforms]
        self.erules = [e(self) for e in edge_transforms]

    def transform_sentence (self, tree, graph):
        '''Transform the tree according to the rules and add
        resulting nodes and edges to the graph'''
        nodes = self.process_nodes(tree)
        deps = self.extract_dependencies(tree)
        deps.reverse()
        edges = self.process_edges(nodes, deps)
        nodes, edges = self.post_process(nodes, edges)
        self.add_to_graph(nodes, edges, graph)

    def process_nodes (self, tree):
        nodes = {}
        for ms in tree['tokens']:
            sem = {'id':ms['id']}
            for rule in self.nrules:
                if rule.match(ms):
                    rule.transform(ms, sem)
            nodes[sem['id']] = sem
        return nodes

    def extract_dependencies (self, tree):
        deps = deque([(tree['dependencies'][0],None)])
        edges = []
        while len(deps)>0:
            d, parent = deps.popleft()
            if parent:
                edges.append((d['function'], parent, d['token']))
            for c in d.get('children', []):
                deps.append((c,d['token']))
        return edges

    def process_edges (self, nodes, deps):
        edges = []
        for d in deps:
            for rule in self.erules:
                fun, head, child = d[0], nodes[d[1]], nodes[d[2]]
                if rule.match(fun, head, child):
                    edges.append(rule.transform(fun, head, child))
        return edges

    def post_process (self, nodes, edges):
        return nodes, edges

    def add_to_graph (self, nodes, edges, graph):
        tokens = {}
        for k in nodes:
            node = nodes[k]
            if 'concept' in node:
                tokid = node['id']
                del node['id']
                nid = graph.add_node(node['concept'], node)
                tokens[tokid] = nid
        for fun, head, child, gram in edges:
            if head in tokens and child in tokens:
                graph.add_edge(head=tokens[head],
                        dependent=tokens[child],
                        functor=fun, gram=gram)
