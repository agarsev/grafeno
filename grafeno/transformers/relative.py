from grafeno.transformers.interrogative import Transformer as Interrogative

class Transformer (Interrogative):

    def transform_dep (self, dep, pid, cid):
        edge = super().transform_dep(dep, pid, cid)
        if dep == 'relcl':
            edge['functor'] = 'RESTR'
        return edge

    def post_process (self):
        super().post_process()
        for e in self.edges:
            if e.get('functor') == 'RESTR':
                referent = e['parent']
                subord_verb = e['child']
                for f in self.edges:
                    if f.get('parent', None) == subord_verb:
                        obj = self.nodes[f['child']]
                        if obj.get('concept') == '?':
                            f['child'] = referent
                            del obj['concept']
