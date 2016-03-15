#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup
import urllib2
import time
import re


def sogou_extract_urls(sogou_serp):
    result_urls = []
    soup = BeautifulSoup(sogou_serp)
    h3s = soup.find_all(class_='vrTitle') + soup.find_all(class_='pt')
    for h3 in h3s:
        url = h3.a['href'].strip()
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
        if not retry:
            result_urls.append('')

    return result_urls


if __name__ == '__main__':
    queries = open('../query.txt', 'r').readlines()
    for i in range(0, 10):
        query = queries[i].strip()
        sogou_serp = open('../SERP_sogou/' + query + '_sogou.html', 'r').read()
        result_urls = sogou_extract_urls(sogou_serp)
        print result_urls
