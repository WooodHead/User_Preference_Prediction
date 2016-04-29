#coding=utf8
__author__ = 'luocheng'


'''

几个类：

    debugger是一个调试工具，没啥用
    slot是一条结果，不区分是垂搜结果还是普通的结果
    parser是一个parse结果页的工具，其中入口的函数是parseSERP,返回的是一个slot的列表

    各个字段说明:

    title 每条结果不管垂直还是普通的，都有一个字体比较大的title，抽取的是title
    summary 对于普通结果来说，是一个我们通常意义下的摘要，对于垂直结果，可能没有这一字段，我把垂直结果所有的呈现在页面上的文字都抽出来了，放在other text里面。
    othertext 见上一条
    rank 现在是从结果的tag,例如uigs_rb_9最后一个数字代表的是排序，这个排序不考虑广告，垂直结果和普通结果是整合在一起的
    resulttype 直接把结果的tag弄上去了，可以分析结果的类型
    links，对于一些结果，其中可能有不止title一个点击链接，特别是垂直结果，链接特别多，比如说 北京大学结果页里，就有百度百科北京大学这个结果，下面有有一些链接是直接可以点击的，我把这些结果抽出来，anchor text,url 作为一个pair放在links这个list里了。
    foot 普通结果下面，有一个结果的说明，比如，天龙八部搜狐视频的结果下面，有一个 “搜狐视频 - tv.sohu.com/s2012/tlbb2013/ - 2012-12-31”，这些字都丢在foot里面了，没有进一步解析
    showsource, showurl，showtime这三个字段暂时没用，可以从foot这个字段里面提取
    其他：
    网页文件和输出的文件都是utf8编码，osx 下对大规模网页测试过没问题。

'''

import urllib2
import re
import os
from bs4 import *
import bs4
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class debuger:
    def __init__(self, filename):
        self.filename = filename
        self.fout = open(self.filename, 'w')

    def write(self, content):
        self.fout.write(content)

    def close(self):
        self.fout.close()


class Slot:
    def __init__(self):
        self.title = ''
        self.summary = ''
        self.mainurl = ''
        self.othertext = ''
        self.links = list()
        self.rank = -1
        self.resulttype = ''
        self.foot = ''
        self.showedSource = ''
        self.showedURL = ''
        self.showedTime = ''
        self.figure = ''
        self.vertical_dictionary = {}


class Parser:
    def textstrip(self, node):
        rtr = ''
        for l in node.get_text().split('\n'):
            if l.strip() != '':
                rtr = rtr+l.strip()+' '
        return rtr

    def parsePairs(self, node):
        rtr = []
        for item in node.find_all('a'):
            if 'href' in item.attrs:
                rtr.append((self.textstrip(item), item['href']))
        return rtr

    def parseFoot(self, node):
        rtr = ''
        for item in node.find_all('cite'):
            if 'id' in item.attrs:
                if 'cacheresult_info' in item['id']:
                    rtr = self.textstrip(item)
        return rtr

    def parseSummary(self, node):
        rtr = ''
        for item in node.find_all('div'):
            if 'id' in item.attrs:
                if 'cacheresult_summary' in item['id']:
                    rtr = self.textstrip(item)
        return rtr

    def parseFigure(self, node):
        item = node.find_all('img')
        if len(item) != 0:
            rtr = 1
        else:
            rtr = 0
        return rtr

    def parseTitle(self, node):
        titlelist = node.find_all('h3')
        if len(titlelist) > 0:
            for h3node in titlelist:
                for item in h3node.children:
                    if item.name == 'a':
                        text = ''
                        url = ''
                        tp = ''
                        rank = -1
                        for l in item.get_text().split('\n'):
                            if l.strip() != '':
                                text = text+l.strip()+' '
                        if 'href' in item.attrs:
                            url = item['href']
                        if 'id' in item.attrs:
                            tp = item['id']
                            if tp.split('_')[-1].isdigit():
                                rank = int(tp.split('_')[-1])
                        return text.strip(), url, tp, rank
        return '', '', 'None', -1

    def parsevrTitle(self, node):
        titlelist = node.find_all('h3') + node.find_all('div')
        if len(titlelist) > 0:
            for titlenode in titlelist:
                if u'class' in titlenode.attrs:
                    classvalues = titlenode['class']
                    if 'vrTitle' in classvalues:
                        for item in titlenode.children:
                            if item.name == 'a':
                                text = ''
                                url = ''
                                tp = ''
                                rank = -1
                                for l in item.get_text().split('\n'):
                                    if l.strip() != '':
                                        text = text+l.strip()+' '
                                if 'href' in item.attrs:
                                    url = item['href']
                                if 'id' in item.attrs:
                                    tp = item['id']
                                    if tp.split('_')[-1].isdigit():
                                        rank = int(tp.split('_')[-1])
                                return text.strip(), url, tp, rank
        return '', '', 'None', -1

    def parseDiv(self, node, tp):
        rtr = Slot()
        if tp == 'vrwrap':
            rtr.title, rtr.mainurl, rtr.resulttype, rtr.rank = self.parsevrTitle(node)
            rtr.summary = self.parseSummary(node)
            rtr.foot = self.parseFoot(node)
            rtr.othertext = self.parseOtherText(node)
            rtr.figure = self.parseFigure(node)
            rtr.vertical_dictionary = self.parseVeritcalCategory(node, rtr.mainurl)

        if tp == 'rb':
            rtr.title, rtr.mainurl, rtr.resulttype, rtr.rank = self.parseTitle(node)
            rtr.summary = self.parseSummary(node)
            rtr.foot = self.parseFoot(node)
            rtr.othertext = self.parseOtherText(node)
            rtr.figure = self.parseFigure(node)
            rtr.vertical_dictionary = self.parseVeritcalCategory(node, rtr.mainurl)

        return rtr

    def parseOtherText(self, node):

        text = ''
        tp = type(node)

        if tp == bs4.element.Tag:
            if node.name == 'h3':
                # print 'hit h3'
                return ''
            if node.name == 'script':
                # print 'hit script'
                return ''
            if node.name == 'div':
                if 'id' in node.attrs:
                    if 'cacheresult_summary' in node['id']:
                        return ''
                if 'class' in node.attrs:
                    if 'fb' in node['class']:
                        return ''
            if node.name == 'style':
                return ''
            childrens = node.children
            childrens2 = node.children
            cldlength = len(list(childrens2))
            if cldlength == 0:
                # print 'leaf',node.name
                text = self.textstrip(node)
            else:
                for item in childrens:
                    text = text + ' ' + self.parseOtherText(item)

        if tp == bs4.element.NavigableString:
            rtr = ''
            for l in node.string.split('\n'):
                if l.strip() != '':
                    rtr = rtr+l.strip() + ' '

            return rtr

        return text

    def parseVeritcalCategory(self, node, url):
        vertical_dictionary = {}
        category_name = ["encyclopedia", "gps_map", "forum", "download", "image", "image_text", "video", "news", "experience", "reading", "others"]
        for item in category_name:  # initialization
            vertical_dictionary[item] = 0
        if "baike" in url:
            vertical_dictionary["encyclopedia"] = 1

        # for item in node.find_all('div'):
        nodes = node.find_all('h3') + node.find_all('div')
        for h3node in nodes:
            for item in h3node.find_all('a'):
                if 'id' in item.attrs:
                    if 'sogou_vr_30001302' in item['id'] or 'sogou_vr_30001009' in item['id']:
                        vertical_dictionary["encyclopedia"] = 1

                    if 'sogou_vr_10000801' in item['id']:
                        vertical_dictionary["gps_map"] = 1

                    if "sogou_vr_30000901" in item['id'] or "sogou_vr_30000401" in item['id'] or "sogou_vr_30000402" in item['id'] or "sogou_vr_30002401" in item['id'] or "sogou_vr_30010028" in item['id']:
                        vertical_dictionary["forum"] = 1

                    if "sogou_vr_30002003" in item['id'] or "sogou_vr_30000201" in item['id'] or "sogou_vr_30000202" in item['id'] or "sogou_vr_30010052" in item['id']:  # wenwen or zhidao
                        vertical_dictionary["forum"] = 1

                    if "sogou_vr_30002300" in item['id'] or "sogou_vr_30001903" in item['id']:
                        vertical_dictionary["download"] = 1

                    if 'sogou_vr_10000103' in item['id'] or "sogou_vr_30002201" in item['id']:
                        vertical_dictionary["image"] = 1

                    if "sogou_vr_30000909" in item['id'] or "sogou_vr_30010020" in item['id']:
                        vertical_dictionary["image_text"] = 1

                    if "sogou_vr_700531" in item['id'] or "sogou_vr_300014" in item['id'] or 'sogou_vr_10000201' in item['id'] or 'sogou_vr_30010053' in item['id'] or "sogou_vr_70043819" in item['id'] or "sogou_vr_30001531" in item['id'] or 'sogou_vr_30010054' in item['id']:
                        vertical_dictionary["video"] = 1

                    if "sogou_vr_30000501" in item['id'] or "sogou_vr_11002501" in item['id']:
                        vertical_dictionary["news"] = 1

                    if "sogou_vr_30010007" in item['id'] or "sogou_vr_30010008" in item['id']:
                        vertical_dictionary["experience"] = 1

                    if "sogou_vr_300801" in item['id'] or "sogou_vr_30001702" in item['id'] or "sogou_vr_30001703" in item['id'] or "sogou_vr_30010005" in item['id'] or "sogou_vr_30010006" in item['id']:
                        vertical_dictionary["reading"] = 1

                    for i in range(1, 10):
                        if "sogou_vr_" + str(i) in item['id']:
                            flag = True
                            for tp in category_name:
                                if vertical_dictionary[tp] != 0:
                                    flag = False
                                    break
                            if flag:
                                vertical_dictionary["others"] = 1
                                break

        return vertical_dictionary

    def parseSERP(self, filename):
        soup = BeautifulSoup(open(filename).read())
        return self.parseSERPSoup(soup)

    def parseSERPContents(self, contents):
        soup = BeautifulSoup(contents)
        return self.parseSERPSoup(soup)

    def parseSERPSoup(self, soup):
        rtr = list()
        for cld in soup.find_all('div'):
            if u'class' in cld.attrs and u'id' in cld.attrs:
                if cld[u'class'] == [u'main'] and cld[u'id'] == u'main':
                    for div in cld.find_all('div'):
                        if u'class' in div.attrs:
                            classvalues = div['class']
                            if 'vrwrap' in classvalues:
                                parseresult = self.parseDiv(div,'vrwrap')
                                if parseresult.rank != -1:
                                    rtr.append(parseresult)
                            if 'rb' in classvalues:
                                parseresult = self.parseDiv(div,'rb')
                                if parseresult.rank != -1:
                                    rtr.append(parseresult)

        return rtr


def unit():
    db = debuger('test.txt')
    p = Parser()
    files = os.listdir('/Users/luocheng/Documents/pycharmproj/serp')
    for f in files:
        print f
        resultlist = p.parseSERP('/Users/luocheng/Documents/pycharmproj/serp/'+f)
        for item in resultlist:
            db.write('file:'+str(f)+'\t'+'rank:'+str(item.rank)+'\t'+'type:'+item.resulttype+'\t'+'title:'+item.title+'\t'+'summary:'+item.summary+'\tothertext:'+item.othertext+'\n')
            # print 'file:',f,'rank:',item.rank,'type:',item.resulttype,'title:',item.title,'summary:',item.summary,'othertext:',item.othertext
    db.close()

if __name__ == '__main__':
    p = Parser()
    resultlist = p.parseSERP('temp.html')
    import json
    for item in resultlist:
        print item.rank, item.title, item.mainurl
        print json.dumps(item.__dict__, ensure_ascii=False).encode('utf-8')
