from conceptgraphs.grammar import TGrammar

default_sempos = {
    'noun': 'n',
    'verb': 'v',
    'adjective': 'j',
    'adverb': 'r'
}

class Grammar (TGrammar):

    def __init__ (self, sempos = default_sempos):
        self.pos_list = sempos.keys()
        self.pos_dict = sempos

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        pos = msnode.get('pos')
        if pos in self.pos_list:
            sem['concept'] = msnode.get('lemma')
            sem['sempos'] = self.pos_dict[pos]
        return sem
