class Transformer:
    '''This class is the basic transformer class. Other transformers should
    inherit from it either directly or indirectly.

    Transformer composition in `grafeno` uses cooperative inheritance. When a
    new module is written, it should extend the base class, or it can extend one
    or more other transformers which provide some required functionality. This
    is a way of managing dependencies, since the base classes will be inserted
    by Python into the inheritance chain.

    The new module can then extend the methods it is interested in, adding
    some processing to that stage. However, for the chaining to work, every
    extended method has to make sure to:

    1. Call ``super()`` with the correct (original) arguments at the very beggining of the function body.
    2. Return the appropriate value, either modified, or untouched as returned from ``super()``.

    Some attributes are present in the transformer during processing. They can
    be used and modified in the appropriate stages.

    Parameters
    ----------
    graph : :py:mod:`Graph <grafeno.graph>`
        The graph to which all transformed text will be added.
    lang : string
        Language code to use for parsing, and available to any subclassing
        transformers.

    Attributes
    ----------
    graph : :py:mod:`Graph <grafeno.graph>`
        The graph to which all transformed text will be added.
    stage : string
        Useful for debugging or checking, this string denotes what stage the
        processing is currently in.
    nodes : dict of :ref:`semantic nodes <semantic_nodes>`
        Available from pre_process up to post_process.
        Map of semantic nodes obtained for the sentence being processed, indexed
        by id.
    edges : list of :ref:`semantic edges <semantic_edges>`
        Available from pre_process up to post_process.
        List of semantic edges obtained for the sentence being processed.
    '''

    def __init__ (self, graph=None, lang='en', **kwds):
        self.stage = ""
        self.lang = lang
        self.graph = graph

    def transform_text (self, text):
        '''Transforms a list of sentences into the semantic graph.

        It shouldn't be overriden.'''
        self.stage = "before_all"
        self.before_all()
        self.stage = "parse_text"
        sentences = self.parse_text(text)
        for tree in sentences:
            self.stage = "pre_process"
            self.pre_process(tree)
            self.stage = "transform"
            self.transform_tree(tree)
            self.stage = "post_process"
            self.post_process()
            self.stage = "add_to_graph"
            self._id_map = self._add_to_graph()
            self.stage = "post_insertion"
            self.post_insertion(list(self._id_map.values()))
        self.stage = "after_all"
        self.after_all()
        self.stage = ""

    def parse_text (self, text):
        '''
        Return a list of dependency treees.
        '''
        raise NotImplementedError("A parsing transformer should be used")

    def pre_process (self, tree):
        '''Prepares the transformer for processing a new sentence. Transformers
        can extend this method to initialize per-sentence variables.

        Parameters
        ----------
        tree : dict
            The dependency parse of the sentence.
        '''
        self.nodes = {} # ID -> dict { concept }
        self.edges = [] # dict { parent(ID), child(ID), functor }

    def transform_node (self, msnode):
        '''Transform a morphosyntactic node to a semantic one.

        Transformers should extend this module if any processing should occur
        for individual nodes.

        The parser module should add to it an `id` property with the temporary
        id to use to refer to it.

        Parameters
        ----------
        msnode : dict
            Dictionary of morphosyntactic tags

        Returns
        -------
        :ref:`semantic node <semantic_nodes>`
        '''
        return {}

    def transform_dep (self, dependency, parent, child):
        '''Transforms a dependency relation into a semantic edge.

        Transformers should extend this module if any processing should occur
        for each dependency relation.

        Parameters
        ----------
        dependency : string
            Name of the dependency relation.
        parent, child : int
            Temporary ids of the source and target semantic nodes. Note that
            these provisional nodes might not turn into true semantic nodes in
            the graph, if they don't have a `concept` attribute by the end of
            processing.

        Returns
        -------
        :ref:`semantic edge <semantic_edges>`
        '''
        return { 'parent': parent,
                 'child': child }

    def merge (self, a, b):
        '''TODO: maybe this should be moved to the utils transformer.

        Combine two nodes by id. Update all outgoing and incoming edges. All
        properties of b are lost, the ones in a are kept. a can be an existing
        graph node, b should be a node currently being processed.

        .. note:: Can be done only during post_process.
        '''
        if self.stage != 'post_process':
            raise AssertionError("merge must be called during post_process")
        del self.nodes[b]
        for edge in self.edges:
            if edge.get('parent') == b:
                edge['parent'] = a
            if edge.get('child') == b:
                edge['child'] = a
            if edge.get('parent', '-') == edge.get('child', 'x') and 'functor' in edge:
                del edge['functor']

    def post_process (self):
        '''This method is called after all nodes and dependency relations are
        processed. Sentence-level processing should be done here, as well as any
        node or edge merging or destruction.

        Even though there are no parameters or return values, extenders should
        still call ``super()`` at the beggining. Semantic nodes and edges are
        available in the transformer's (self) ``nodes`` and ``edges``
        properties.
        '''
        pass

    def _add_to_graph (self):
        g = self.graph
        real_id = {}
        for id, node in self.nodes.items():
            if 'concept' in node:
                nid = g.add_node(**node)
                real_id[id] = nid
        for edge in self.edges:
            if 'functor' in edge:
                parent = edge.pop('parent')
                child = edge.pop('child')
                g.add_edge(real_id.get(parent, parent),
                           real_id.get(child, child), **edge)
        return real_id

    def post_insertion (self, sentence_nodes):
        '''Called after the processed nodes and edges are added to the semantic
        graph. It is useful if some processing needs the real graph ids of the
        new nodes.

        Parameters
        ----------
        sentence_nodes : list of ids
            The definitive (graph) ids of the nodes that were produced by
            analyzing the current sentence.
        '''
        pass

    def before_all (self):
        '''Called at the beggining of processing a full text, before any sentences.'''
        pass

    def after_all (self):
        '''Called at the end of processing a full text, after all sentences.'''
        pass
