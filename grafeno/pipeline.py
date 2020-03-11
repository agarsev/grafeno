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
'''
The pipeline module allows the user to write full pipelines of experiments in a
dict, which can then be loaded and run by the library with one function call::

   from grafeno import pipeline

   experiment = {
       'text': 'Colorless green ideas sleep furiously.',
       'parser': 'freeling', 
       'transformers': [ 'all' ],
       'linearizers': [ 'triplets' ]
   }

   result = pipeline.run(experiment)
   print(result)

Pipeline Formatting
-------------------
The following attributes for the pipeline dict are supported.

.. note::

    The pipeline is designed so that it can be easily serialized and loaded
    from a string format such as YAML, making repeatable experiments as easy
    as writing into a text file what operations to perform, and with what
    arguments.

.. rubric:: Input
Input to the pipeline is required. It can be an already constructed `graph`,
otherwise `text`, `parser` and `transformers` will be needed.

- `graph`: a :py:mod:`Graph <grafeno.graph>`
- `text`: a raw natural language text.
- `parser`: what parser to use to process the text. Possible values are:
    - ``freeling``: http://nlp.lsi.upc.edu/freeling/node/1
    - ``spacy``: https://spacy.io

    .. note::

        This is just a shortcut for using as first transformer a module named
        ``<parser_type>_parser``. This allows parsers to be changed easily and
        independently from the rest of the pipeline.

    .. warning::

        To use a specific parser, it must be installed and available to grafeno.
        For *freeling*, the `analyze` executable must be in the path, in the
        case of *spacy*, the module must be importable.

- `transformers`: list of transformer names to use (see :py:mod:`grafeno.transformers`)
- `transformer_args`: dict of arguments for the `transformers`

.. rubric:: Operation
- `operations`: a list of dicts, each with an ``op`` attribute with the
  operation name, and the rest of the arguments to be used as parameters for
  the operation.

.. rubric:: Output
A text if a `linearizers` attribute is present, otherwise the raw `graph`
obtained is returned.

- `linearizers`: list of linearizer names to use (see :py:mod:`grafeno.linearizers`)
- `linearizer_args`: dict of arguments for the linearizers

.. seealso::

    Some pre-built pipelines can be found in the ``config`` directory,
    written in YAML: :ref:`configs`.

'''

from grafeno import Graph as CG, transformers, linearizers
from grafeno.operations import operate

DEF_PARSER = 'spacy'
DEF_TRANSFORMERS = ['all']
DEF_T_ARGS = {}
DEF_LINEARIZERS = []
DEF_L_ARGS = {}

def run (pipeline):
    '''Run a complete pipeline of graph operations.

    Parameters
    ----------
    pipeline : dict
        The pipeline description.

    Returns
    -------
        The result from running the pipeline with the provided arguments.
    '''

    # INPUT
    if 'graph' in pipeline:
        graph = pipeline['graph']
    elif 'text' in pipeline:
        ts = []
        try:
            ts.append(pipeline.get('parser', DEF_PARSER)+'_parse')
        except KeyError:
            pass
        try:
            ts += pipeline.get('transformers', DEF_TRANSFORMERS)
            T = transformers.get_pipeline(ts)
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
        operation['op'] = name

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
