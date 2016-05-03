from conceptgraphs.transformer import Transformer as Base

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.graph.gram['node_from_concept'] = dict()

    def pre_process (self, tree):
        super().pre_process(tree)
        self.reused_nodes = []
        self.sentence_concepts = {}

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        concept = sem.get('concept')
        node_dict = self.graph.gram['node_from_concept']
        # Only one node for each concept
        if concept in node_dict:
            del sem['concept']
            nid = node_dict[concept]
            sem['id'] = nid
            self.reused_nodes.append(nid)
        elif concept in self.sentence_concepts:
            del sem['concept']
            nid = self.sentence_concepts[concept]
            sem['id'] = nid
            self.reused_nodes.append(nid)
        elif concept:
            self.sentence_concepts[concept] = sem['id']
        return sem

    def post_insertion (self, sentence_nodes):
        super().post_insertion(sentence_nodes + self.reused_nodes)
        g = self.graph
        # Record the concept nodes
        for n in sentence_nodes:
            concept = g._g.node[n]['concept']
            g.gram['node_from_concept'][concept] = n
