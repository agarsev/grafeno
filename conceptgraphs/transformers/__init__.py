from importlib import import_module

i = lambda n: import_module(n, __name__)

transformer_dict = {
    'deep': i('.deep_grammar').Transformer,
    'extend': i('.extend').Transformer,
    'lesk_link': i('.lesk_link').Transformer,
    'pos_extract': i('.pos_extract').Transformer,
    'sentences': i('.sentence_record').Transformer,
    'sim_link': i('.similarity_link').Transformer,
    'unique': i('.unique_nodes').Transformer,
    'wordnet': i('.wordnet_get').Transformer,
}

pipeline_cache = transformer_dict.copy()

def get_pipeline (modules):
    '''Takes a list of transformers and returns a transformer which
    subclasses them all'''
    name = '__'.join(modules)
    if name in pipeline_cache:
        return pipeline_cache[name]
    else:
        T = type(name, tuple(transformer_dict[m] for m in reversed(modules)), {})
        pipeline_cache[name] = T
        return T
