from grafeno.linearizers.node_edges import Linearizer as Base

default_node_gram_blacklist = ( 'id', 'sempos' )
default_edge_gram_blacklist = ( 'functor' )
default_sempos_map = {
    'n': 'NOUN',
    'v': 'VERB',
    'j': 'ADJECTIVE',
    'r': 'ADVERB'
}

def cypher_dict_print (dict):
    if len(dict)>0:
        return (' {'
            +', '.join('{}: {!r}'.format(k, str(dict[k])) for k in dict)
            +'}')
    else:
        return ''

class Linearizer (Base):

    def __init__ (self,
                  node_gram_blacklist = default_node_gram_blacklist,
                  node_gram_whitelist = None,
                  edge_gram_blacklist = default_edge_gram_blacklist,
                  edge_gram_whitelist = None,
                  sempos_map = default_sempos_map,
                  footer = '',
                  **kwds):
        cypher_footer = '\nMATCH (n) REMOVE n._temp_id;'+footer
        super().__init__(footer=cypher_footer, **kwds)
        self.node_gram_blacklist = node_gram_blacklist
        self.node_gram_whitelist = node_gram_whitelist
        self.edge_gram_blacklist = edge_gram_blacklist
        self.edge_gram_whitelist = edge_gram_whitelist
        self.sempos_map = sempos_map


    def process_node (self, node):
        if self.node_gram_whitelist:
            gram = { key:node[key] for key in node
                    if key in self.node_gram_whitelist }
        else:
            gram = { key:node[key] for key in node
                    if key not in self.node_gram_blacklist }
        gram['_temp_id'] = node['id']
        return 'CREATE (n:{}{});'.format(
            self.sempos_map.get(node['sempos']),
            cypher_dict_print(gram))

    def process_edge (self, n, m, edge):
        if self.edge_gram_whitelist:
            gram = { key:edge[key] for key in edge
                    if key in self.edge_gram_whitelist }
        else:
            gram = { key:edge[key] for key in edge
                    if key not in self.edge_gram_blacklist }
        return ('MATCH (n {{_temp_id:\'{}\'}}), (m {{_temp_id: \'{}\'}}) '
                'CREATE (n)-[r:{}{}]->(m);').format(n, m, edge['functor'], cypher_dict_print(gram))
