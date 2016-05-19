from collections import deque

class Transformer:

    def __init__ (self, graph=None):
        self.graph = graph

    def transform_text (self, sentences):
        self.before_all()
        for s in sentences:
            self.transform_sentence(s)
        self.after_all()

    def transform_sentence (self, tree):
        '''Transform the tree according to the rules and add
        resulting nodes and edges to the graph'''
        self.pre_process(tree)
        self.process_nodes(tree)
        deps = self.extract_dependencies(tree)
        deps.reverse()
        self.process_edges(deps)
        self.post_process()
        sentence_nodes = self.add_to_graph()
        self.post_insertion(sentence_nodes)

    def pre_process (self, tree):
        self.nodes = {} # ID -> dict { concept }
        self.edges = [] # dict { parent(ID), child(ID), functor }

    def process_nodes (self, tree):
        for ms in tree['tokens']:
            sem = self.transform_node(ms)
            if sem:
                self.nodes[ms['id']] = sem

    def transform_node (self, msnode):
        '''take a morfosyntactic node (dict) and return a semantic node (dict).
        Semantic nodes get dropped in the end if they don't have a concept
        attribute.'''
        return {}

    def extract_dependencies (self, tree):
        root = tree['dependencies'][0]
        deps = deque([(c, root['token']) for c in root.get('children', [])])
        ret = []
        while True:
            try:
                d, parent = deps.popleft()
            except IndexError:
                break
            ret.append((d['function'], parent, d['token']))
            for c in d.get('children', []):
                deps.append((c,d['token']))
        return ret

    def process_edges (self, deps):
        for name, parent, child in deps:
            try:
                self.edges.append(self.transform_dep(name, parent, child))
            except KeyError:
                continue

    def transform_dep (self, dependency, parent, child):
        '''take a dependency relation (str) and the parent and child node ids
        and return a semantic edge (dict). Semantic edges get
        dropped in the end if they don't have a functor attribute.'''
        return { 'parent': parent,
                 'child': child }

    def post_process (self):
        pass

    def add_to_graph (self):
        g = self.graph
        real_id = {}
        for id, node in self.nodes.items():
            if 'concept' in node:
                nid = g.add_node(**node)
                real_id[id] = nid
        for edge in self.edges:
            if 'functor' in edge:
                parent = edge.pop('parent')
                child = edge.pop('child')
                g.add_edge(real_id.get(parent, parent),
                           real_id.get(child, child), **edge)
        return real_id.values()

    def post_insertion (self, sentence_nodes):
        pass

    def before_all (self):
        pass

    def after_all (self):
        pass
