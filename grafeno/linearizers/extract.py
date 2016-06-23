class Linearizer ():

    def __init__ (self, summary_length=100, summary_margin=10,
            normalize_sentence_scores=False, graph=None):
        self.graph = graph
        self.__length = summary_length
        self.__margin = summary_margin
        self.__norm = normalize_sentence_scores

    def score_sentence (self, sentence_nodes):
        return 0

    def linearize (self):
        g = self.graph
        if self.__norm:
            sentence_scores = [self.score_sentence(s)/len(s) if len(s) else 0 for s in g.gram['sentence_nodes']]
        else:
            sentence_scores = [self.score_sentence(s) for s in g.gram['sentence_nodes']]

        best = sorted(range(len(sentence_scores)), reverse=True, key=lambda i:sentence_scores[i])
        length = 0
        last = 0
        full = g.gram['sentences']
        while length < self.__length and last<len(best):
            length += len(full[best[last]].split(' '))
            if length < self.__length + self.__margin:
                last += 1
        return '\n'.join(s for i, s in enumerate(full) if i in best[:last])
