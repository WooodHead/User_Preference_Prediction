#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup


def clean_sogou_html(query, html):
    soup = BeautifulSoup(html)
    delete_list = []
    delete_list.append(soup.select("dl.topbar"))
    delete_list.append(soup.select("div.header"))
    delete_list.append(soup.select("div#right"))
    delete_list.append(soup.select("div.hintBox"))
    delete_list.append(soup.select("div#pagebar_container"))
    delete_list.append(soup.select("div#s_bottom_form"))
    delete_list.append(soup.select("div#s_footer"))
    delete_list.append(soup.select(".results > .jzwd"))
    delete_list.append(soup.select("#main > .safetips"))
    for every in delete_list:
        if len(every) > 0:
            every[0].extract()

    sponsored = soup.select("div.sponsored")
    if len(sponsored) > 0:
        for every in sponsored:
            every.extract()
    bizs = soup.select(".biz_effect")
    if len(bizs) > 0:
        for biz in bizs:
            biz.extract()
    bizrbs = soup.select("[class~=biz_rb]")
    if len(bizrbs) > 0:
        for biz in bizrbs:
            biz.extract()
    wrap = soup.select(".wrap")
    if len(wrap) > 0:
        results = wrap[0].select(".results")
        if len(results) == 0:
            wrap[0].extract()

    head = soup.select("head")
    if len(head) > 0:
        ori_tag = head[0]
        new_tag = soup.new_tag("style")
        ori_tag.append(new_tag)
        new_tag.string = r"html { overflow-x:hidden; }"

    wrapper = soup.select("div#wrapper")
    if len(wrapper) > 0:
        wrapper[0]['style'] = "padding-top: 5px; padding-left: 15px"

    results = soup.select("#main .results > div")
    if len(results) > 10:
        for result in results[10:]:
            result.extract()

    fout = open('../../annotation_platform/static/SERP_sogou/' + query + '_sogou.html', 'w')
    fout.write(str(soup).replace("搜狗", "").replace("百度", ""))
    fout.close()


if __name__ == '__main__':
    f_query = open('../data/query.txt', 'r')
    for i in range(0, 2087):
        print i
        query = f_query.readline().strip()
        html = open('../SERP_sogou/' + query + '_sogou.html', 'r').read()
        clean_sogou_html(query, html)
    f_query.close()
