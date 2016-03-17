#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

import urllib2
import time
import random


def extract_bing(query):
    url = "https://www.bing.com/search?q="
    url += urllib2.quote(query)
    url += "&ie=utf-8"
    retry = 3
    while retry > 0:
        try:
            req_timeout = 5
            header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
            req = urllib2.Request(url, None, header)
            resp = urllib2.urlopen(req, None, req_timeout)
            html = resp.read()
            # print html
            fout = open('../SERP_bing/' + query + '_bing.html', 'w')
            print html
            fout.write(html)
            fout.close()
            break
        except urllib2.URLError, e:
            print 'url error:', e
            time.sleep(60)
            retry = retry - 1
            continue
        except Exception, e:
            print 'error:', e
            retry = retry - 1
            time.sleep(60)
            continue

query_file = open("../data/query.txt", "r")
queries = query_file.readlines()
count = 0
# load_user_agent()
for query in queries:
    query = query.replace("\n", "")
    try:
        extract_bing(query)
        random_time_s = random.randint(5, 10)
        time.sleep(random_time_s)
        print query
        count += 1
        if count % 10 == 0:
            count = 0
            random_time = random.randint(60, 120)
            time.sleep(random_time)
    except:
        continue
