class Linearizer ():

    def __init__ (self, header='', separator='', footer='', graph=None):
        self.graph = graph
        self.separator = separator
        self.header = header
        self.footer = footer

    def linearize (self):
        nodes = self.get_root_nodes()
        nodes = self.expand_node_list(nodes)
        words = (self.process_node(n) for n in nodes)
        nonempty = [(w, n) for w, n in zip(words, nodes) if w is not None]
        try:
            words, nodes = (list(l) for l in zip(*nonempty))
        except ValueError:
            return ''
        self.apply_boundaries(words, nodes)
        return self.concat(words)

    def get_root_nodes (self):
        return [min(self._g.nodes())]

    def expand_node_list (self, nodes):
        change = True
        while change is True:
            change = False
            next_nodes = []
            for n in nodes:
                try:
                    expanded = n.get('expanded')
                except AttributeError:
                    n = self.graph.node[n].copy()
                    expanded = False
                if expanded:
                    next_nodes.append(n)
                else:
                    next_nodes += self.expand_node(n)
                    change = True
            nodes = next_nodes
        return nodes

    def expand_node (self, n):
        n['expanded'] = True
        return [n]

    def process_node (self, n):
        return n['concept']

    def apply_boundaries (self, words, nodes):
        for i in range(len(nodes)):
            if i == 0:
                left = None
            else:
                left = nodes[i-1]
            if i == len(nodes)-1:
                right = None
            else:
                right = nodes[i+1]
            words[i] = self.boundary(left, nodes[i], words[i], right)

    def boundary (self, left, n, word, right):
        return word

    def concat (self, nodes):
        return self.header+self.separator.join(nodes)+self.footer

