from grafeno.transformers.base import Transformer as Base

# TODO: this should be a linearizer or operation, not a transformer

translation_table = {
    'ATTR': 'is',
    'HYP': 'isa'
}

class Transformer (Base):

    def post_process (self):
        super().post_process()
        for edge in self.edges:
            if 'class' in edge:
                if edge.get('functor') == 'COMP':
                    edge['functor'] = 'is_'+edge['class']
                else:
                    edge['functor'] = edge['class']
            elif 'functor' in edge:
                edge['functor'] = translation_table.get(edge['functor'], edge['functor'])


