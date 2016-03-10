#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

import urllib2
import time
import random


def load_user_agent():
    fp = open('./user_agents', 'r')
    line = fp.readline().strip('\n')
    while line:
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()

user_agents = list()


def extract_bing(query):
    url = "http://cn.bing.com/search?hl=zh&q="
    url += urllib2.quote(query)
    retry = 3
    while retry > 0:
        try:
            req_timeout = 5
            length = len(user_agents)
            index = random.randint(0, length-1)
            user_agent = user_agents[index]
            header = {'user-agent': user_agent}
            req = urllib2.Request(url, None, header)
            resp = urllib2.urlopen(req, None, req_timeout)
            html = resp.read()
            #print html
            fout = open('./SERP_bing/' + query + '_bing.html', 'w')
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

query_file = open("./query.txt", "r")
queries = query_file.readlines()
count = 0
load_user_agent()
for query in queries:
    query = query.replace("\n", "")
    try:
        extract_bing(query)
        random_time_s = random.randint(5, 10)
        time.sleep(random_time_s)
        print query
        count += 1
        if count % 10 == 9:
            count = 0
            random_time = random.randint(240, 360)
            time.sleep(random_time)
    except:
        continue
