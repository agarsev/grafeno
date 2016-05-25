from conceptgraphs import Graph as CG, transformers, linearizers
from conceptgraphs.operations import operate

DEF_TRANSFORMERS = ['semantic']
DEF_T_ARGS = {}
DEF_LINEARIZERS = []
DEF_L_ARGS = {}

# Pipeline: a dict
#
# Input: either graph or text and transformers
# * graph: a CGraph to recover
# * text: a raw natural language text
# * transformers: array of transformer names to use
# * transformer_args: (optional) dict of arguments for the transformers
#
# Operations: an array of dicts, with "op" for the operation name, and the rest
#   arguments to be passed to the operation
#
# Output: either graph or text if linearizers arg is present
# * linearizers: array of linearizers to use
# * linearizer_args: (optional) dict of arguments for the linearizers

def run (pipeline):

    # INPUT
    if 'graph' in pipeline:
        graph = pipeline['graph']
    elif 'text' in pipeline:
        try:
            T = transformers.get_pipeline(pipeline.get('transformers', DEF_TRANSFORMERS))
        except KeyError:
            raise ValueError("Unknown transformer pipeline")
        T_args = pipeline.get('transformer_args', DEF_T_ARGS)
        graph = CG(transformer=T,transformer_args=T_args,text=pipeline['text'])
    else:
        raise ValueError('Must provide either graph or text')

    # OPERATIONS
    for operation in pipeline.get('operations', []):
        try:
            name = operation.pop('op')
        except KeyError:
            raise ValueError("No name for the operation")
        try:
            graph = operate(graph, name, **operation)
        except TypeError as e:
            raise ValueError(e)

    # OUTPUT
    if 'linearizers' in pipeline:
        try:
            L = linearizers.get_pipeline(pipeline.get('linearizers', DEF_LINEARIZERS))
        except KeyError:
            raise ValueError("Unknown linearizer pipeline")
        L_args = pipeline.get('linearizer_args', DEF_L_ARGS)
        return graph.linearize(linearizer=L,linearizer_args=L_args)
    else:
        return graph
