from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def transform_node (self, ms):
        sem = super().transform_node(ms)
        if 'concept' in sem:
            if sem['concept'].isnumeric():
                sem['concept'] = "'"+sem['concept']+"'"
        return sem
