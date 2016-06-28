.. _configs:

Pre-built Pipelines
===================

Some pre-built pipelines come with the library's source code. They are stored
under the directory ``configs``. The script ``test.py`` can load them with the
``-c`` flag, and ``server.py`` automatically finds them and serves them in the web
service.

Summarization
-------------

This pipeline is used for extracting short summaries out of news documents.

.. literalinclude:: ../configs/summary.yaml

Concept maps
------------

This pipeline generates concept maps useful for conceptual blending.
Additionally, it linearizes them into a prolog triplet format.

.. literalinclude:: ../configs/conceptmap.yaml
