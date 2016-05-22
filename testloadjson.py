# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
import json
from tree_serial import *

def treeFromJSON(name):
    path = os.path.dirname(os.path.abspath(__file__)) + '/' + name + '.json'
    json_file = open(path, 'r')
    data = json.loads(json_file.read())
    return build(data)
