from grafeno.transformers.pos_extract import Transformer as PosExtract

modmapping = {
    'modnomatch': 'EQ',
    'conj': False
}
defaultrel = 'ATTR'

class Transformer (PosExtract):
    '''Processes noun grammatemes and noun-noun modifications, such as apposition.'''

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
        if 'concept' in p and 'concept' in c and p.get('sempos') == 'n' and c.get('sempos') == 'n':
            functor = modmapping.get(dep, defaultrel)
            if functor:
                edge['functor'] = functor
        return edge
