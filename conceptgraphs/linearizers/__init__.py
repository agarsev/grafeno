import glob
from importlib import import_module
from os.path import dirname, basename, isfile

linearizers = dict()

for m in glob.glob(dirname(__file__)+"/*.py"):
    f = basename(m)[:-3]
    if isfile(m) is True and not f.startswith('__'):
        linearizers[f] = import_module('.'+f, __name__).Linearizer

def get_pipeline (modules):
    '''Takes a list of linearizers and returns a linearizer which
    subclasses them all'''
    name = '__'.join(modules)
    if name in linearizers:
        return linearizers[name]
    else:
        T = type(name, tuple(linearizers[m] for m in reversed(modules)), {})
        linearizers[name] = T
        return T
