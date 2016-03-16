#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup
import urllib2
import time
import re


def baidu_extract_urls(baidu_serp):
    result_urls = []
    soup = BeautifulSoup(baidu_serp)
    content_left = soup.find('div', id='content_left')
    if content_left:
        h3s = content_left.find_all('h3')
        for h3 in h3s:
            if not ('class' in h3.attrs and (h3['class'] == ['t'] or h3['class'] == ['t', 'c-gap-bottom-small'])):
                continue
            try:
                url = h3.a['href'].strip()
            except:
                continue
            retry = 3
            while retry:
                try:
                    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
                    req = urllib2.Request(url, None, header)
                    resp = urllib2.urlopen(req, None, 5)
                    html = resp.read()
                    soup_ = BeautifulSoup(html)
                    if soup_.title:
                        url = resp.geturl()
                        result_urls.append(url)
                    else:
                        urlp = re.compile(r'<script>window.location.replace\("(.*?)"\)</script>')
                        url = urlp.search(html).group(1)
                        result_urls.append(url)
                    break
                except:
                    retry -= 1
                    continue

    return result_urls


if __name__ == '__main__':
    queries = open('../query.txt', 'r').readlines()
    for i in range(0, 10):
        query = queries[i].strip()
        baidu_serp = open('../SERP_baidu/' + query + '_baidu.html', 'r').read()
        result_urls = baidu_extract_urls(baidu_serp)
        print result_urls
