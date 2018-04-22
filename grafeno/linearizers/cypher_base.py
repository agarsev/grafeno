from grafeno.linearizers.node_edges import Linearizer as Base

default_node_gram_blacklist = ( 'id' )
default_edge_gram_blacklist = ( 'functor' )
default_sempos_map = {
    'n': 'NOUN',
    'v': 'VERB',
    'j': 'ADJECTIVE',
    'r': 'ADVERB'
}

def cypher_labels (labels):
    if labels and len(labels)>0:
        return ':'+':'.join(labels)
    else:
        return ''

def cypher_gram (gram):
    if gram and len(gram)>0:
        return (' {'
            +', '.join('{}: {!r}'.format(k, str(gram[k])) for k in gram)
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
                  cypher_extra_params = {},
                  **kwds):
        super().__init__(**kwds)
        self.node_gram_blacklist = node_gram_blacklist
        self.node_gram_whitelist = node_gram_whitelist
        self.edge_gram_blacklist = edge_gram_blacklist
        self.edge_gram_whitelist = edge_gram_whitelist
        self.sempos_map = sempos_map
        self.cypher_extra_params = cypher_extra_params

    def process_node (self, node):
        return self.cypher_format_node(node,
            self.cypher_get_node_labels(node),
            self.cypher_get_node_gram(node))

    def cypher_format_node (self, node, labels, gram):
        return self.cypher_print_node('n', labels, gram)

    def cypher_get_node_labels (self, node):
        return [self.sempos_map.get(node['sempos'])]

    def cypher_get_node_gram (self, node):
        if self.node_gram_whitelist:
            node_gram = { key:node[key] for key in node
                    if key in self.node_gram_whitelist }
        else:
            node_gram = { key:node[key] for key in node
                    if key not in self.node_gram_blacklist }
        node_gram.update(self.cypher_extra_params)
        return node_gram

    def process_edge (self, n, m, edge):
        return self.cypher_format_edge(n, m, edge,
            self.cypher_get_edge_labels(edge),
            self.cypher_get_edge_gram(edge))

    def cypher_format_edge (self, head, child, edge, labels, gram):
        return '{}{}{}'.format(head, child,
            self.cypher_print_edge('r', labels, gram))

    def cypher_get_edge_labels (self, edge):
        return [edge['functor']]

    def cypher_get_edge_gram (self, edge):
        if self.edge_gram_whitelist:
            return { key:edge[key] for key in edge
                    if key in self.edge_gram_whitelist }
        else:
            return { key:edge[key] for key in edge
                    if key not in self.edge_gram_blacklist }

    def cypher_print_node (self, id, labels, gram):
        return '({}{}{})'.format(id,
            cypher_labels(labels),
            cypher_gram(gram))

    def cypher_print_edge (self, id, labels, gram):
        return '-[{}{}{}]->'.format(id,
            cypher_labels(labels),
            cypher_gram(gram))

