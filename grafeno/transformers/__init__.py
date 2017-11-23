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
:py:mod:`Transformers <grafeno.transformers.base>` are one of the key objects of
the `grafeno` library. They are in charge of converting the dependency parse of
a sentence, extracted by an external tool, into a `grafeno` semantic graph.

::

    from grafeno import Graph as CG
    from grafeno.transformers import get_pipeline

    T = get_pipeline(['pos_extract', 'wordnet', 'unique'])
    g = CG(transformer=T, transformer_args={}, text="Fish fish fish fish fish fish fish.")

This process happens in stages. First, morphological nodes are transformed
into semantic ones:

.. _semantic_nodes:

.. rubric:: Semantic nodes

Semantic nodes are dictionaries with the following
attributes:

- ``concept``: if present, the node will be added to the semantic
  graph. It represents the main idea, or meaning, of the node. If there is no
  `concept`, no semantic node will be produced corresponding to the
  morphological one.
- ``id``: a temporal identifier for the node while it is being
  processed, and hasn't thus been added to the graph yet. When the node
  is finally added to the graph, it will be changed to the proper graph
  ID.

Other attributes in the dictionary are also added to the
semantic graph node, and are referred to as `grammatemes`.

After the nodes have been processed, the dependency relations are transformed
into semantic edges:

.. _semantic_edges:

.. rubric:: Semantic edges

Each semantic edge is a dictionary with the following attributes:

- ``parent``: the (temporal or otherwise) id of the source node.
- ``child``: the (temporal or otherwise) id of the target node.
- ``functor``: if present, the edge will be added to the semantic graph. The
  `functor` represents the semantic relation between the `parent` and `child`
  nodes.

Other attributes in the dictionary will be also added to the
semantic graph edge, and are referred to as `grammatemes`.

Apart from the main operations of node and edge transformations, there are
additional stages in the process where previous or further processing can
happen. In order to construct this collection of processing stages, a
`Transformer` object has to be created. For this, a :py:mod:`base <grafeno.transformers.base>`
class is provided, which has methods for the different stages and is in charge
of calling them at the right time and with the appropriate arguments.

The way to construct a pipeline is thus to inherit from this :py:mod:`base <grafeno.transformers.base>`
class, and extend the appropriate methods. See its documentation for more
information on them.

Additionally, the idea behind transformer classes is that each is supposed to
perform a specific operation. This way, a transforming pipeline can be
constructed by mixing and matching the desired transformers, by way of creating
a class which inherits from them. In order to make this operation easier, a
convenience function is provided: :py:mod:`grafeno.transformers.get_pipeline`,
which takes a list of transformers to use, and constructs the appropriate class
which inherits from them all in the correct order.
'''

import glob
from importlib import import_module
from os.path import dirname, basename, isfile

transformers = dict()

def _get_single_transformer (name):
    if name in transformers:
        return transformers[name]
    else:
        transformers[name] = import_module('grafeno.transformers.'+name, __name__).Transformer
        return transformers[name]

def get_pipeline (modules):
    '''Takes a list of transformers and returns a transformer class which
    subclasses them all'''
    name = '__'.join(modules)
    if name in transformers:
        return transformers[name]
    else:
        T = type(name, tuple(_get_single_transformer(m) for m in reversed(modules)), {})
        transformers[name] = T
        return T
