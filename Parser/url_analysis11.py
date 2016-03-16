#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from Baidu_extract_url import *
from Sogou_extract_url import *
import urllib2


class url:
    def urlSimilar(self, url_a, url_b):
        if url_a == '' or url_b == '':
            return 0
        else:
            if url_a == url_b:
                return 1
            else:
                return 0

    def urlJaccard(self, baidu_urls, sogou_urls):
        count1 = 0
        l_baidu = len(baidu_urls)
        l_sogou = len(sogou_urls)
        print l_baidu, l_sogou
        for i in range(0, l_baidu):
            for j in range(0, l_sogou):
                flag = self.urlSimilar(baidu_urls[i], sogou_urls[j])
                if flag:
                    count1 += 1
                    break
        print count1
        jaccard = float(count1)/float(l_sogou + l_baidu - count1)
        return jaccard


def compute_Jaccard(baidu_urls, sogou_urls):
    return url().urlJaccard(baidu_urls, sogou_urls)


def url_analysis():
    queries = open('../query.txt', 'r').readlines()
    fout = open('../data/url_jaccard1.csv', 'w')
    for i in range(2000, len(queries)):
        query = queries[i].strip()
        try:
            baidu_serp = open('../SERP_baidu/' + query + '_baidu.html', 'r').read()
            sogou_serp = open('../SERP_sogou/' + query + '_sogou.html', 'r').read()
            baidu_urls = baidu_extract_urls(baidu_serp)
            sogou_urls = sogou_extract_urls(sogou_serp)
            jaccard = compute_Jaccard(baidu_urls, sogou_urls)
            print query, jaccard
            fout.write(query + ',' + str(jaccard) + '\n')
        except:
            continue
    fout.close()

if __name__ == '__main__':
    url_analysis()
