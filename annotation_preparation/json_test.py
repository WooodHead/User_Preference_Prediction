#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

try:
    import simplejson as json
except ImportError:
    import json

with open('query_part_1', 'r') as fin:
    for line in fin:
        obj = json.loads(line)
        query = unicode(obj['query'])
        print query
