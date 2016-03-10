#!/usr/bin/env python3

from subprocess import Popen, PIPE
import subprocess as subp
import json

def parse (sentence):
    proc = Popen(["analyze", "--flush", "-f", "en.cfg", "--outlv", "dep", "--output", "json"], stdin=PIPE, stdout=PIPE)
    data, err = proc.communicate(sentence.encode('UTF-8'))
    return json.loads("["+data.decode('UTF-8')+"]")
