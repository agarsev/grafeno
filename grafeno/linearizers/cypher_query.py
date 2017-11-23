from grafeno.linearizers.cypher_base import Linearizer as CypherBase
from grafeno.graph import Graph as CG

class Linearizer (CypherBase):
    '''This linearizer converts the graph into a Cypher_ query, suitable for
    running against a Neo4J database.
    
    The created query matches against subgraphs in the database with **at
    least** the same nodes and relations. If there are more nodes in the graph
    database, it also matches. If some node or relation in the grafeno graph is
    not present in the database subgraph, the whole subgraph doesn't match.

    If there are any question nodes (``concept = '?'``) in the graph, the query
    finds the equivalent node in the database, and returns it and its full
    directed subcomponent. To reconstruct it, see :func:`reconstruct_graphs`.

    If there are no question nodes in the query, the number of matches is
    returned.

    .. _Cypher: https://neo4j.com/docs/developer-manual/current/cypher/
    '''

    def __init__ (self, **kwds):
        super().__init__(
            node_header='MATCH\n',
            node_sep=',\n',
            node_gram_whitelist=['concept','sempos','polarity'],
            edge_header=',\n',
            edge_sep=',\n',
            footer='\nRETURN count(*)',
            **kwds)
        self.__variable_idx = 0
        self.__variable_dict = dict()

    def filter_node (self, node):
        if node['concept'] == '?':
            self.__variable_dict[node['id']] = 'what'
            self.footer = '\nOPTIONAL MATCH path = (what)-[*..4]->()\nRETURN DISTINCT what, path'
            return False
        return True

    def cypher_format_node (self, node, labels, gram):
        id = 'x{}'.format(self.__variable_idx)
        self.__variable_idx += 1
        self.__variable_dict[node['id']] = id
        return self.cypher_print_node(id, labels, gram)

    def cypher_format_edge (self, head, child, edge, labels, gram):
        return '({}){}({})'.format(
            self.__variable_dict[head],
            self.cypher_print_edge('', labels, gram),
            self.__variable_dict[child])

def _reconstruct_single_graph (root, paths):
    g = CG()
    id_map = dict()
    root_id = g.add_node(**root)
    id_map[root.id] = root_id
    g.roots = [root_id]
    for path in paths:
        for node in path.nodes:
            if node.id not in id_map:
                id_map[node.id] = g.add_node(**node)
        for rel in path.relationships:
            g.add_edge(id_map[rel.start], id_map[rel.end], rel.type, **rel)
    return g

def reconstruct_graphs (results):
    '''This function can be used to reconstruct a grafeno concept graph from the
    results returned by a query from Neo4J created with the
    :class:`cypher_query linearizer <Linearizer>`.

    ::

        from grafeno.linearizers.cypher_query import Linearizer as graph_to_cypher_query, reconstruct_graphs
        query = query_graph.linearize(linearizer=graph_to_cypher_query)

        from neo4j.v1 import GraphDatabase
        driver = GraphDatabase.driver(**connection_params)
        results = driver.session().run(query)

        for graph in reconstruct_graphs(results):
            do_something_with(graph)
    '''
    components = dict()
    for record in results.records():
        root = record['what']
        if root.id in components:
            component = components[root.id]
        else:
            component = [root]
            components[root.id] = component
        path = record['path']
        if path:
            component.append(path)
    return [ _reconstruct_single_graph(paths[0],paths[1:])
            for paths in components.values() ]
