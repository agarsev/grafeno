from importlib import import_module

i = lambda n: import_module(n, __name__)

transformer_dict = {
    'deep': i('.deep_grammar').Transformer,
    'extend': i('.extend').Transformer,
    'lesk_link': i('.lesk_link').Transformer,
    'pos_extract': i('.pos_extract').Transformer,
    'sentence_record': i('.sentence_record').Transformer,
    'sim_link': i('.similarity_link').Transformer,
    'unique_nodes': i('.unique_nodes').Transformer,
    'wordnet_get': i('.wordnet_get').Transformer,
}
