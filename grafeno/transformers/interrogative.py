from grafeno.transformers.pos_extract import Transformer as PosExtract

class Transformer (PosExtract):

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        tag_pos = msnode.get('tag', msnode.get('pos'))
        if tag_pos and tag_pos.startswith('w'):
            sem['concept'] = '?'
        return sem
