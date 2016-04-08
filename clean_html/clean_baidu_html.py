#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup


def clean_baidu_html(query, html):
    soup = BeautifulSoup(html)
    delete_list = []
    delete_list.append(soup.select("div#head"))
    delete_list.append(soup.select("div#s_tab"))
    delete_list.append(soup.select("div#content_right"))
    delete_list.append(soup.select("div.head_nums_cont_inner"))
    delete_list.append(soup.select("div#foot"))
    delete_list.append(soup.select("div#rs"))
    delete_list.append(soup.select("div#page"))
    delete_list.append(soup.select("div.leftBlock"))
    delete_list.append(soup.select("div.head_nums_cont_outer"))
    for every in delete_list:
        if len(every) > 0:
            every[0].extract()
    zFfoim = soup.select("div.zFfoim")
    if len(zFfoim) > 0:
        for every in zFfoim:
            every.extract()
    head = soup.select("head")
    if len(head) > 0:
        ori_tag = head[0]
        new_tag = soup.new_tag("style")
        ori_tag.append(new_tag)
        new_tag.string = r"html { overflow-x:hidden; }"
    spons = soup.select("#content_left > [class~=smixKl]")
    if len(spons) > 0:
        for spon in spons:
            spon.extract()

    wrapper_wrapper = soup.select("div#wrapper_wrapper")
    if len(wrapper_wrapper) > 0:
        scripts = wrapper_wrapper[0].select("script")
        if len(scripts) > 0:
            tip_script = scripts[len(scripts) - 1]
            tip_script.extract()
    content_left = soup.select("div#content_left")
    if len(content_left) > 0:
        content_left[0]['style'] = "padding-left: 15px"
    fout = open('../' + query + '_baidu.html', 'w')
    fout.write(str(soup).replace("百度", "").replace("搜狗", ""))
    fout.close()


if __name__ == '__main__':
    check_querys = ['窗花的剪法', '龙珠国语', '腾讯游戏大全', '怎样开红酒瓶塞', '金铃怨攻略']
    for query in check_querys:
        fin = open('../' + query + '_baidu.html', 'r')
        html = fin.read()
        fin.close()
        clean_baidu_html(query, html)
