from conceptgraphs.transformer import Transformer as Base

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        if not hasattr(self, 'node_from_concept'):
            self.node_from_concept = dict()

    def pre_process (self, tree, graph):
        super().pre_process(tree, graph)
        self.reused_nodes = []
        self.sentence_concepts = {}

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        concept = sem.get('concept')
        # Only one node for each concept
        if concept in self.node_from_concept:
            del sem['concept']
            nid = self.node_from_concept[concept]
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

    def post_insertion (self, sentence_nodes, graph):
        super().post_insertion(sentence_nodes + self.reused_nodes, graph)
        # Record the concept nodes
        for n in sentence_nodes:
            concept = graph._g.node[n]['concept']
            self.node_from_concept[concept] = n
