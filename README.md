Nilfusion
=========

Workflow and code for concept extraction and operation.

Usage
-----

Put in a folder `data` the data to analyze. If it's an html file, it must have
the extension `.html`. If it's plain text, the extension should be `.txt`.

Run `make`, this should run the whole pipeline for the data.

For extra configuration, write a `local.mk` file and put there extra options.

Requirements
------------
- python3
- beautifulsoup4
- freeling

Authors
-------
- Antonio F. G. Sevilla <afgs@ucm.es>
- Alberto Fernández Isabel <afernandezisabel@ucm.es>
