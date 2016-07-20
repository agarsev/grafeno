from grafeno.transformers.pos_extract import Transformer as PosExtract

import re

modre = re.compile('mod')

class Transformer (PosExtract):
    '''Processes noun grammatemes and noun-noun modifications, such as aposition
    (creates ``EQ`` edges).'''

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        sempos = sem.get('sempos')
        if sempos == 'n':
            sem['proper'] = msnode.get('type') == 'proper'
            sem['num'] = msnode.get('num','p')
        return sem

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        p = self.nodes[pid]
        c = self.nodes[cid]
        if modre.match(dep) and 'concept' in p and 'concept' in c and p.get('sempos') == 'n' and c.get('sempos') == 'n':
            edge['functor'] = 'EQ'
        return edge
