from grafeno.linearizers.cypher_base import Linearizer as CypherBase

class Linearizer (CypherBase):

    def __init__ (self, footer='', **kwds):
        super().__init__(
            footer='\nMATCH (n) REMOVE n._temp_id;'+footer,
            **kwds)

    def cypher_format_node (self, node, labels, gram):
        gram['_temp_id'] = node['id']
        return 'CREATE {};'.format(self.cypher_print_node('n', labels, gram))

    def cypher_format_edge (self, head, child, edge, labels, gram):
        return 'MATCH {}, {} CREATE (n){}(m);'.format(
            self.cypher_print_node('n', None, {'_temp_id':head}),
            self.cypher_print_node('m', None, {'_temp_id':child}),
            self.cypher_print_edge('r', labels, gram))
