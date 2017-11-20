from copy import copy

from grafeno.graph import Graph as CG

def graft (stem, locus, bud, root):
    '''
    This operation inserts a whole semantic graph (the `bud`) in place of a node in
    another graph (the `stem`).
    
    It could be used to replace interrogative nodes in a question graph with the
    answer graph, or to reify exophoric relations.

    .. note::

        If the `bud` is not connected, all components will be inserted into
        `stem`, but only the `locus` and `root` nodes will be merged.

    .. warning::

        This operation is destructive. If you want to keep a non-modified
        version of `stem`, copy it first.

    Parameters
    ----------
    stem : Graph
        The concept graph into which the `bud` is going to be inserted.
    locus : int
        ID of the node in `stem` to be replaced with `bud`.
    bud : Graph
        The concept graph to insert into `stem`.
    root : int
        ID of the node in `bud` that is going to replace the locus, taking with
        it all its sub-graph.
    '''
    id_map = dict()
    for n in bud.nodes():
        nid = n['id']
        if nid == root:
            stem.node[locus] = copy(n)
            stem.node[locus]['id'] = locus
            id_map[nid] = locus
        else:
            id_map[nid] = stem.add_node(**n)
    for head, child, edge in bud.all_edges():
        stem.add_edge(id_map[head], id_map[child], **edge)
