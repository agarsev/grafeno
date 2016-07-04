from grafeno.linearizers.extract import Linearizer as Extract

class Linearizer (Extract):

    def __init__ (self, hub_score=2, nonhub_score=1, **kwds):
        super().__init__(**kwds)
        self.__hub_score = hub_score
        self.__nonhub_score = nonhub_score
        clusters = self.graph.gram['clusters']
        # TODO: add more heuristics
        best_cluster = max(range(len(clusters)), key=lambda i: len(clusters[i]))
        if 'HVS' in self.graph.gram:
            self.__hvs = self.graph.gram['HVS'][best_cluster]
        else:
            self.__hvs = []
        self.__cluster = clusters[best_cluster]

    def score_sentence (self, sentence_nodes):
        score = super().score_sentence(sentence_nodes)
        for o in sentence_nodes:
            if o in self.__hvs:
                score += self.__hub_score
            elif o in self.__cluster:
                score += self.__nonhub_score
        return score
