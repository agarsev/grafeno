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
'''This is the main package for the grafeno library. If you want to use grafeno
from your code, import it like this::

    import grafeno

If you only need specific functionality, you may want to import it like this::

    from grafeno import Graph as CG, pipeline

'''

from grafeno.graph import Graph
import grafeno.pipeline as pipeline
