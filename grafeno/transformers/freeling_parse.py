from grafeno.transformers.base import Transformer as Base

from collections import deque
from subprocess import Popen, PIPE
import subprocess as subp
import os
import json
import re

regex = re.compile('}\s*{')

class Transformer (Base):

    def __init__ (self, **kwds):
        super().__init__(**kwds)
        self.__config = os.path.dirname(__file__)+"/freeling_conf/"+self.lang+".cfg"
        self._parser = 'freeling'

    def parse_text (self, text):
        '''Calls the freeling process to obtain the dependency parse of a text.'''
        proc = Popen(["analyze", "--flush", "-f", self.__config], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        data, err = proc.communicate(text.encode('UTF-8'))
        return json.loads('['+regex.sub('},{',data.decode('UTF-8'))+']')

    def transform_tree (self, tree):
        self.deps = self.__extract_dependencies(tree)
        self.deps.reverse()
        self.__process_nodes(tree)
        self.__process_edges(self.deps)

    def __process_nodes (self, tree):
        for ms in tree['tokens']:
            temp_id = ms['id']
            self.__current_temp_id = temp_id
            self.nodes[temp_id] = self.transform_node(ms)

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        sem['id'] = self.__current_temp_id
        return sem

    def __process_edges (self, deps):
        for name, parent, child in deps:
            try:
                self.edges.append(self.transform_dep(name, parent, child))
            except KeyError:
                continue

    def __extract_dependencies (self, tree):
        root = tree['dependencies'][0]
        deps = deque([(c, root['token']) for c in root.get('children', [])])
        ret = []
        while True:
            try:
                d, parent = deps.popleft()
            except IndexError:
                break
            ret.append((d['function'], parent, d['token']))
            for c in d.get('children', []):
                deps.append((c,d['token']))
        return ret
