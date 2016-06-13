# Grafeno -- Python concept graphs library
# Copyright 2016 Antonio F. G. Sevilla <afgs@ucm.es>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from grafeno import Graph as CG, transformers, linearizers
from grafeno.operations import operate

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
