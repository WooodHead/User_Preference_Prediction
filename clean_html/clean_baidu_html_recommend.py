#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

f_query = open('../data/query.txt', 'r')
i = 0
while True:
    print i
    i += 1
    query = f_query.readline().strip()
    if not query:
        break
    try:
        fin = open('../../annotation_platform/static/SERP_baidu/' + query + '_baidu.html', 'r')
        html = fin.read()
        fin.close()
        fout = open('../../annotation_platform/static/SERP_baidu/' + query + '_baidu.html', 'w')
        fout.write(html.replace(r" src='https://ss1.bdstatic.com/5eN1bjq8AAUYm2zgoY3K/r/www/cache/static/protocol/https/global/js/all_async_search_rcmd_6fcb1787.js'", '').replace(r" src='https://ss1.bdstatic.com/5eN1bjq8AAUYm2zgoY3K/r/www/cache/static/protocol/https/global/js/all_async_search_a582e6e2.js'", ''))
        fout.close()
    except:
        continue
