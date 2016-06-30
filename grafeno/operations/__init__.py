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

from grafeno import Graph as CG

from grafeno.operations.clustering2 import cluster
from grafeno.operations.markov_clustering import cluster as markov_cluster
from grafeno.operations.spot_domain import spot_domain
from grafeno.operations.filters import filter_edges

def operate (graph, operation, **args):

    if operation == 'cluster':
        HVS, clusters = cluster(graph, **args)
        graph.gram['HVS'] = HVS
        graph.gram['clusters'] = clusters
        return graph

    if operation == 'spot_domain':
        subgraph, main_entity = spot_domain(graph, **args)
        r = CG(graph, subgraph=subgraph)
        r.gram['main_entity'] = main_entity
        return r

    if operation == 'filter_edges':
        filter_edges(graph, **args)
        return graph

    if operation == 'markov_cluster':
        clusters = markov_cluster(graph, **args)
        graph.gram['clusters'] = clusters
        return graph

    raise ValueError("Unknown operation")
