#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'
try:
    import simplejson as json
except ImportError:
    import json

for i in range(1, 41):
    fin = open('query_part_' + str(i), 'r')
    odd = 0
    even = 0
    while True:
        line = fin.readline().strip()
        if not line:
            break
        jsonobj = json.loads(line)
        query = jsonobj['query']
        try:
            f_html = open('../../annotation_platform/static/SERP_baidu/' + query + '_baidu.html', 'r')
            f_html.close()
            f_html = open('../../annotation_platform/static/SERP_sogou/' + query + '_sogou.html', 'r')
            f_html.close()
        except:
            print query
        length = len(query)
        if length % 2 == 0:
            even += 1
        else:
            odd += 1
    print i, odd, even, odd + even
    fin.close()

