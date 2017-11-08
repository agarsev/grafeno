from grafeno.linearizers.cypher_base import Linearizer as CypherBase

class Linearizer (CypherBase):

    def __init__ (self, **kwds):
        super().__init__(
            node_header='MATCH\n',
            node_sep=',\n',
            node_gram_whitelist=['concept'],
            edge_header=',\n',
            edge_sep=',\n',
            footer='\nRETURN count(*)',
            **kwds)
        self.__variable_idx = 0
        self.__variable_dict = dict()

    def filter_node (self, node):
        if node['concept'] == '?':
            self.__variable_dict[node['id']] = 'what'
            self.footer = ',\npath = (what)-[*..4]->()\nRETURN path'
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
