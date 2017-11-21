# Grafeno -- Python concept graphs library
# Copyright 2016 Antonio F. G. Sevilla <afgs@ucm.es>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
'''
This module provides the main Graph class. Graph objects are the core of the
library, and most operations revolve around manipulating them.

::

    from grafeno import Graph as CG

    g = CG(transformer = MyTransformer)
    print(g.linearize(linearizer = MyLinearizer))

'''

import json
import networkx as nx
from networkx.readwrite import json_graph

class Graph:
    '''Semantic graph class. Nodes represent concepts, while edges stand for the
    relations between them.

    Parameters
    ----------
    transformer : :py:mod:`Transformer <grafeno.transformers>`, optional
        If provided, it will be used to transform all text added to the graph
        into semantic nodes and edges.
    transformer_args : dict, optional
        Arguments for the `transformer` class.
    text : string, optional
        If provided, this text will be added to the graph (transformed with the
        `transformer` class).
    original : Graph, optional
        If provided, the new graph will be initialized with the existing
        information in `original`.
    subgraph : bunch of nodes
        If `original` and `subgraph` are provided, only the nodes in `subgraph`
        will be copied over from `original`.

    Attributes
    ----------
    gram : dict
        dictionary of parameters global to the conceptual graph.
    node : dict
        dictionary of concept nodes, indexed by node id.
    '''

    def __init__ (self, original=None, transformer=None, transformer_args={}, text=None, subgraph=None, from_networkx=None):
        if from_networkx:
            self._g = from_networkx
            self._next_node = max(n['id'] for _, n in from_networkx.nodes(data=True))+1
        elif original:
            self._next_node = original._next_node
            if subgraph:
                self._g = nx.DiGraph(original._g.subgraph(subgraph))
            else:
                self._g = nx.DiGraph(original._g)
        else:
            self._next_node = 0
            self._g = nx.DiGraph()
        self.gram = self._g.graph
        self.node = self._g.node
        if transformer:
            self.transformer = transformer(graph=self, **transformer_args)
        if text:
            self.add_text(text)

    # Building the graph

    def add_node (self, concept, **gram):
        '''Creates a concept node in the graph.

        Parameters
        ----------
        concept : string
            The (non-unique) textual representation of the concept node.
        gram : keyword args, optional
            Additional 'grammatemes', a free-form python dict of attributes to
            attach to the node.

        Returns
        -------
        int
            The graph id of the newly created node.
        '''
        nid = self._next_node
        self._next_node += 1
        gram['id'] = nid
        self._g.add_node(nid, concept=concept, **gram)
        return nid

    def add_edge (self, head, dependent, functor, **gram):
        '''Creates a semantic edge between two concept nodes in the graph.

        Parameters
        ----------
        head, dependent : node_id
            The graph ids of the nodes to link. The edge is directed, from head
            to dependent.
        functor : string
            The textual representation of the _functor_, the name of the
            relation between the concepts.
        gram : keyword args, optional
            Additional 'grammatemes', a free-form python dict of attributes to
            attach to the edge.

        Raises
        ------
        ValueError
            When the head or dependent id's are not valid.
        '''
        if head not in self._g or dependent not in self._g:
            raise ValueError('Head or dependent are not in the graph ('+str(functor)+')')
        self._g.add_edge(head, dependent, functor=functor, **gram)

    def add_text (self, text):
        '''Processes a text, and adds the resulting nodes and edges to the
        graph.

        Parameters
        ----------
        text : string
            A clean text to process and add to the graph.
        '''
        self.transformer.transform_text(text)

    # Examining the graph
    # TODO: Usage examples with iteration

    def nodes (self):
        '''Returns a list of all the nodes in the graph. Each node is
        represented as a dictionary of concept and further grammatemes.'''
        return [gram for n, gram in self._g.nodes(data=True)]

    def edges (self, nid):
        '''Returns a dictionary of the dependents of a node.

        Parameters
        ----------
        nid : int
            ID of the node

        Returns
        -------
            A dictionary of edges, keyed by neighbor id, and with data
            the grammatemes of the edge.
        '''
        return self._g[nid]

    def all_edges (self):
        '''Iterates over all the edges in the graph.

        Returns
        -------
            An iterator over all the edges of the graph, in the form of tuples
            `(head id, dependent id, edge)`.
        '''
        return self._g.edges(data=True)

    def neighbours (self, node):
        '''Iterates over the neighbours of a node, giving the edge information
        for each neighbour.

        ::

            node = graph.node[0]
            for neighbour, edge in graph.neighbours(node)
                print('{}-{}->{}'.format(
                        node['concept'],
                        edge['functor'],
                        neighbour['concept']))

        Parameters
        ----------
        node : node
            The node in the graph to explore

        Returns
        -------
            An iterator over the neighbours of the node, in the form of tuples
            `(node, edge)`.
        '''
        return ((self.node[mid], edge)
                for mid, edge in self._g[node['id']].items())

    # Output

    def draw (self, bunch=None):
        '''Draws the graph on screen.

        .. note::

            Requires matplotlib and a compatible configured environment.

        Parameters
        ----------
        bunch : list of nodes
            An iterable of node ids to draw, if ``None`` then all nodes are
            included.
        '''
        import matplotlib.pyplot as plt
        if bunch:
            g = self._g.subgraph(bunch)
        else:
            g = self._g
        lay = nx.spring_layout(g)
        nx.draw_networkx_nodes(g,lay,node_size=3000,node_color="white",linewidths=0)
        nx.draw_networkx_labels(g,lay,labels={n:data['concept'] for n, data in g.nodes(True)})
        nx.draw_networkx_edges(g,lay)
        nx.draw_networkx_edge_labels(g,lay,edge_labels={(a,b):data['functor'] for (a,b,data) in g.edges(data=True)})
        plt.show()

    def to_json (self, with_labels = True):
        '''Returns a JSON representation of the graph data.

        Parameters
        ----------
        with_labels : bool
            If True, a 'label' attribute is added to nodes and edges with the
            _concept_ and _functor_, respectively. Useful for further consuming
            by some libraries.

        Returns
        -------
            A string with the graph data encoded in JSON.
        '''
        class BestEffortEncoder(json.JSONEncoder):
            def default(self, obj):
                return repr(obj)
        g = self._g
        if with_labels:
            for n in g:
                node = g.node[n]
                node['label'] = '.'.join(x for x in [node.get('class'),node.get('concept'),node.get('sempos')] if x)
                for m in g[n]:
                    edge = g[n][m]
                    edge['label'] = '.'.join(x for x in [edge.get('functor'),edge.get('class')] if x)
        return json.dumps(json_graph.node_link_data(g), cls=BestEffortEncoder)

    def linearize (self, linearizer=None, linearizer_args={}):
        '''Linearizes a graph into a string.

        Parameters
        ----------
        linearizer : :py:mod:`Linearizer <grafeno.linearizers>`, optional
            If provided, from this point on all linearizations of the graph will
            use an instance of this class. The linearizer is used to transform
            the semantic data, nodes and edges, into a string representation.
        linearizer_args : dict, optional
            Arguments for the `linearizer` class.

        Returns
        -------
            A string, the result of running the linearizer on the graph.
        '''
        if linearizer:
            self.linearizer = linearizer(graph=self, **linearizer_args)
        return self.linearizer.linearize()
