#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from Baidu_extract_url import *
from Sogou_extract_url import *
import urllib2


class url:
    def urlSimilar(self, url_a, url_b):
        print url_a, url_b
        if url_a == '' or url_b == '':
            return 0
        else:
            try:
                html_a = urllib2.urlopen(url_a).read()
                soup_a = BeautifulSoup(html_a)
                title_a = soup_a.head.title.string.strip()
                print title_a
                html_b = urllib2.urlopen(url_b).read()
                soup_b = BeautifulSoup(html_b)
                title_b = soup_b.head.title.string.strip()
                print title_b
                if title_a == title_b:
                    return 1
            except Exception, error:
                print error
                return 0

    def urlJaccard_and_Kendall(self, baidu_urls, sogou_urls):
        count1 = 0
        l_baidu = len(baidu_urls)
        l_sogou = len(sogou_urls)
        print l_baidu, l_sogou
        similar_list = []
        for i in range(0, l_baidu):
            for j in range(0, l_sogou):
                flag = self.urlSimilar(baidu_urls[i], sogou_urls[j])
                if flag:
                    count1 += 1
                    if j not in similar_list:
                        similar_list.append(j)
                    break
        print count1
        jaccard = float(count1)/float(l_sogou + l_baidu - count1)
        count2 = 0
        for i in range(0, len(similar_list)):
            for j in range(i+1, len(similar_list)):
                if similar_list[i] > similar_list[j]:
                    count2 += 1
        print count2
        tau = 1 - float(count2) * 2 / float(l_baidu * (l_baidu - 1))
        return [jaccard, tau]


def compute_Jaccard_and_Kendall(baidu_urls, sogou_urls):
    return url().urlJaccard_and_Kendall(baidu_urls, sogou_urls)


def url_analysis():
    queries = open('../query.txt', 'r').readlines()
    for i in range(0, 1):
        query = queries[i].strip()
        baidu_serp = open('../SERP_baidu/' + query + '_baidu.html', 'r').read()
        sogou_serp = open('../SERP_sogou/' + query + '_sogou.html', 'r').read()
        baidu_urls = baidu_extract_urls(baidu_serp)
        sogou_urls = sogou_extract_urls(sogou_serp)
        print query, compute_Jaccard_and_Kendall(baidu_urls, sogou_urls)

if __name__ == '__main__':
    url_analysis()
