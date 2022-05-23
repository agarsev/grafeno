Grafeno
=======

Python library for concept graph extraction from text, operation, and
linearization. An integrated web service is provided.

This library is still a work in progress, but it has shown to be already useful
for a number of applications, for example extractive text summarization.

Install
-------

Using [poetry](https://python-poetry.org/):

1. `poetry install`
2. If you want to install some extras, run `poetry install --extras "web lexical
   modules"` with the extras that you need (see `pyproject.toml`).
3. `poetry run setup`

To run any grafeno script with poetry, use `poetry run` before the name of the
script and its arguments.

Documentation
-------------
The documentation is a work in progress, so it is a bit patchy, but go ahead and
read it in [ReadTheDocs](http://grafeno.readthedocs.io/en/latest/).

Examples
--------
See the notebooks in the [examples directory](docs/_examples) for how to use grafeno
in different applications.

Web Service
-----------
Run the `server.py` script to get a json web service which exposes most of the
pipeline functionality.

Use `-h` to get the list of options available.

Test script
-----------
A test script is provided in `test.py` that can run a pipeline to test the
library. It can serve as the entry point to the library operation, or as an
example of how to use it from python.

Use `-h` to get the list of options available.

Requirements
------------
- [python](https://www.python.org/) >= 3.4
    - Python packages for use of the library are listed in `requirements.txt`.
      We recommend using [conda](https://conda.io/docs/) to install grafeno and
      its dependencies in a virtual environment.
- A dependency parser. For now, the following are supported:
    - [spaCy](https://spacy.io/) (recommended)
    - [freeling](http://nlp.lsi.upc.edu/freeling/node/1)
- If using the `simplenlg` linearizer, a `java` executable will have to be
  available.

You may also need some NLTK data, for example 'wordnet' and 'wordnet_ic'. They
can be downloaded in python with:
```python
import nltk
nltk.download(['wordnet', 'wordnet_ic'])
```

Authors
-------
- Antonio F. G. Sevilla <afgs@ucm.es>
- Alberto Díaz <albertodiaz@fdi.ucm.es>

Acknowledgements
----------------
The continued development of this library has been possible thanks to a number
of different research and development projects, listed below.

- A collaboration with [MedWhat](https://medwhat.com/), a company that develops
  virtual medical assistant bots and other medical artificial intelligence
  solutions.
- This research is funded by the Spanish Ministry of Economy and Competitiveness
  and the European Regional Development Fund (TIN2015-66655-R (MINECO/FEDER)).
- This work is funded by [ConCreTe](http://nil.fdi.ucm.es/?q=node/780). The project ConCreTe acknowledges the
  financial support of the Future and Emerging Technologies (FET) programme
  within the Seventh Framework Programme for Research of the European
  Commission, under FET grant number 611733.
