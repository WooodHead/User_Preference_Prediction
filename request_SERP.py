# -*- coding: utf-8 -*-
__author__ = 'franky'

import urllib2

from bs4 import BeautifulSoup

base_url = 'https://www.google.com.hk/?gws_rd=ssl&pli=1#safe=strict&q='

def crawler():
    query = 'test'
    url = base_url + query
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    print html
    fout = open(query + '.html', 'w')
    fout.write(html)
    fout.close()

if __name__ == '__main__':
    crawler()
