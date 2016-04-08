from collections import deque

class TGrammar:

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
            sem = self.transform_node(ms)
            nodes[sem['id']] = sem
        return nodes

    def transform_node (self, msnode):
        '''take a morfosyntactic node (dict) and return a semantic node (dict).
        Semantic nodes get dropped in the end if they don't have a concept
        attribute.'''
        return { 'id':msnode['id'] }

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
        return [ self.transform_dep(d[0], nodes[d[1]], nodes[d[2]]) \
                for d in deps ]

    def transform_dep (self, dependency, parent, child):
        '''take a dependency relation (str) and the parent and child nodes
        (semnodes, dict) and return a semantic edge (dict). Semantic edges get
        dropped in the end if they don't have a functor attribute.'''
        return { 'parent': parent['id'],
                 'child': child['id'],
                 'gram': {} }

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
        for edge in edges:
            if 'functor' in edge:
                parent, child = edge['parent'], edge['child']
                if parent in tokens:
                    parent = tokens[parent]
                if child in tokens:
                    child = tokens[child]
                graph.add_edge(head=parent,
                        dependent=child,
                        functor=edge['functor'],
                        gram=edge['gram'])
