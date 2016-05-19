from .base import Transformer as Base

class Transformer (Base):

    def __init__ (self, unique_sempos = None, **kwds):
        super().__init__(**kwds)
        self.__sempos = unique_sempos
        self.graph.gram['node_from_concept'] = dict()

    def post_process (self):
        self.__reused_nodes = []
        usem = self.__sempos
        node_dict = self.graph.gram['node_from_concept']
        first_node = {}
        for nid, node in list(self.nodes.items()):
            if usem and node.get('sempos') not in usem:
                continue
            # Only one node for each concept in unique_sempos
            concept = node.get('concept')
            if concept in first_node:
                self.merge(first_node[concept], nid)
            elif concept in node_dict:
                old = node_dict[concept]
                self.merge(old, nid)
                self.__reused_nodes.append(old)
            elif concept:
                first_node[concept] = nid

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes + self.__reused_nodes)
        g = self.graph
        # Record the concept nodes
        for n in sentence_nodes:
            concept = g.node[n]['concept']
            g.gram['node_from_concept'][concept] = n
