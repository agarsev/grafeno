#!/usr/bin/env python3

from subprocess import Popen, PIPE
import subprocess as subp
import os
import json
import re

regex = re.compile('}\s*{')

def parse (sentence, lang):
    '''Calls the freeling process to obtain the dependency parse of a text.'''
    config = os.path.dirname(__file__)+"/freeling_deps_"+lang+".cfg"
    proc = Popen(["analyze", "--flush", "-f", config], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data, err = proc.communicate(sentence.encode('UTF-8'))
    return json.loads('['+regex.sub('},{',data.decode('UTF-8'))+']')
