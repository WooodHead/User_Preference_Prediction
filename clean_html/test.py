#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

try:
    import simplejson as json
except ImportError:
    import json

for i in range(1, 41):
    f_query = open('../../annotation_platform/annotation_task_user_preference/query_parts/query_part_' + str(i), 'r')
    lines = f_query.readlines()
    print i, len(lines)
    for line in lines:
        jsonobj = json.loads(line.strip())
        query = jsonobj['query']
        fin = open('../../annotation_platform/static/SERP_baidu/' + query + '_baidu.html', 'r')
        fin.close()
    f_query.close()
f_query = open('../../annotation_platform/annotation_task_user_preference/query_parts/query_part_example', 'r')
lines = f_query.readlines()
print len(lines)
for line in lines:
    jsonobj = json.loads(line.strip())
    query = jsonobj['query']
    fin = open('../../annotation_platform/static/SERP_baidu/' + query + '_baidu.html', 'r')
    fin.close()
f_query.close()
