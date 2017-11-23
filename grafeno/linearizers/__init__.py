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

import glob
from importlib import import_module
from os.path import dirname, basename, isfile

linearizers = dict()

def _get_single_linearizer (name):
    if name in linearizers:
        return linearizers[name]
    else:
        linearizers[name] = import_module('grafeno.linearizers.'+name, __name__).Linearizer
        return linearizers[name]

def get_pipeline (modules):
    '''Takes a list of linearizers and returns a linearizer which
    subclasses them all'''
    name = '__'.join(modules)
    if name in linearizers:
        return linearizers[name]
    else:
        T = type(name, tuple(_get_single_linearizer(m) for m in reversed(modules)), {})
        linearizers[name] = T
        return T
