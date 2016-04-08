#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from clean_html import clean_baidu_html
from clean_html import clean_sogou_html


'''fin = open('../data/query.txt', 'r')
lines = 1
part = 1
while part <= 40:
    f_query = open('query_part_' + str(part), 'w')
    querys = 0
    while querys < 50:
        print part, querys
        query = fin.readline().strip()
        lines += 1
        if not query:
            break
        try:
            html_baidu = open('../SERP_baidu/' + query + '_baidu.html', 'r').read()
            html_sogou = open('../SERP_sogou/' + query + '_sogou.html', 'r').read()
            clean_baidu_html.clean_baidu_html(query, html_baidu)
            clean_sogou_html.clean_sogou_html(query, html_sogou)
        except:
            continue
        f_query.write('{"query":"' + query + '"}\n')
        querys += 1
    part += 1
    f_query.close()
fin.close()
print lines'''

'''f_query = open('query_part_example', 'w')
for i in range(0, 2050):
    fin.readline()
for i in range(0, 3):
    query = fin.readline().strip()
    html_baidu = open('../SERP_baidu/' + query + '_baidu.html', 'r').read()
    html_sogou = open('../SERP_sogou/' + query + '_sogou.html', 'r').read()
    clean_baidu_html.clean_baidu_html(query, html_baidu)
    clean_sogou_html.clean_sogou_html(query, html_sogou)
    f_query.write('{"query":"' + query + '"}\n')'''

f_query = open('query_part_checkpoint', 'w')
check_querys = ['窗花的剪法', '龙珠国语', '腾讯游戏大全', '怎样开红酒瓶塞', '金铃怨攻略']
for i in range(0, len(check_querys)):
    query = check_querys[i]
    f_query.write('{"query":"' + query + '"}\n')
