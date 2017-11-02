class Linearizer ():
    '''This linearizer outputs the nodes first, and then the edges.

    Parameters
    ----------
    node_header : string
        A string to print before all other content.
    node_sep : string
        A string to print between nodes.
    edge_header : string
        A string to print after the nodes, and before the edges.
    edge_sep : string
        A string to print between edges.
    footer : string
        A string to print after all other content.
    graph : :py:mod:`Graph <grafeno.graph>`
        The graph to linearize.

    Attributes
    ----------
    graph : :py:mod:`Graph <grafeno.graph>`
        The graph to linearize.
    '''

    def __init__ (self, node_header='', node_sep='\n', edge_header='\n', edge_sep='\n', footer='', graph=None):
        self.graph = graph
        self.node_header = node_header
        self.node_sep = node_sep
        self.edge_header = edge_header
        self.edge_sep = edge_sep
        self.footer = footer

    def linearize (self):
        n_ids = [ n['id'] for n in self.graph.nodes() if self.filter_node(n) ]
        edges = []
        for n in n_ids:
            for m, edge in self.graph.edges(n).items():
                if m in n_ids:
                    edges.append(self.process_edge(n, m, edge))
        node = self.graph.node
        return (self.node_header
            + self.node_sep.join(self.process_node(node[n]) for n in n_ids)
            + self.edge_header
            + self.edge_sep.join(edges)
            + self.footer)

    def filter_node (self, node):
        ''' Override this method to exclude some nodes from the output.

        Parameters
        ----------
        node : dict
            The grammatemes of the node to filter.

        Returns
        -------
        bool
            Whether to include this node (and its edges) in further processing.
        '''
        return True

    def process_node (self, node):
        '''This method generates a string representation of a node. Override to
        customize.

        Parameters
        ----------
        node : dict
            The grammatemes of the node to transform.

        Returns
        -------
        string
            A string representation of the node.
        '''
        return '{}: {}'.format(node['id'], node['concept'])

    def process_edge (self, n, m, edge):
        '''This method generates a string representation of an edge. Override to
        customize.

        Parameters
        ----------
        n : int
            Id of the head node.
        m : int
            Id of the dependent node.
        edge : dict
            Grammatemes of the edge between `n' and `m'.

        Returns
        -------
        string
            A string representation of the edge.
        '''
        return '{}-{}->{}'.format(n, edge['functor'], m)

