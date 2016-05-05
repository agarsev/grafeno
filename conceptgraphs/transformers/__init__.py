import glob
from importlib import import_module
from os.path import dirname, basename, isfile

transformers = dict()

for m in glob.glob(dirname(__file__)+"/*.py"):
    f = basename(m)[:-3]
    if isfile(m) is True and not f.startswith('__'):
        transformers[f] = import_module('.'+f, __name__).Transformer

def get_pipeline (modules):
    '''Takes a list of transformers and returns a transformer which
    subclasses them all'''
    name = '__'.join(modules)
    if name in transformers:
        return transformers[name]
    else:
        T = type(name, tuple(transformers[m] for m in reversed(modules)), {})
        transformers[name] = T
        return T
