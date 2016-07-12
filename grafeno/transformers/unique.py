from grafeno.transformers.index import Transformer as Index

class Transformer (Index):

    def __init__ (self, unique_gram = None, **kwds):
        super().__init__(**kwds)
        self.__gram = unique_gram

    def post_process (self):
        super().post_process()
        self.__reused_nodes = []
        gram = self.__gram
        node_dict = self.node_from_concept
        first_node = {}
        for nid, node in list(self.nodes.items()):
            if gram:
                for attr in gram.keys():
                    if node.get(attr) in gram[attr]:
                        break
                else:
                    continue
            # Only one node for each concept with any of the specified grammatemes
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
        node_dict = self.node_from_concept
        # Record the concept nodes
        for n in sentence_nodes:
            concept = g.node[n]['concept']
            node_dict[concept] = n
