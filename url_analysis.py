#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from SogouParser import *
from BaiduParser import *

class url:
	def urlSimilar(self,url_a,url_b):
		if url_a =="" or url_b=="":
			return 0
		if url_a in url_b or url_b in url_a:
			return 1
		else:
			return 0

	def cleanurl(self, url1):
		url = url1.replace("http://","").replace("www.","").replace(".com/","").replace(".cn","")
		return url


	def urlJaccard(self, baiduSERP,sogouSERP):
		count = 0
		l_baidu = len(baiduSERP)
		l_sogou = len(sogouSERP)
		for i in range(0, l_baidu):
			for j in range(0, l_sogou):
				flag = self.urlSimilar(self.cleanurl(baiduSERP[i]),self.cleanurl(sogouSERP[j].url))
				#if flag:
				#	print cleanurl(baidu[i].url) + "\t" + cleanurl(sogou[j].url)
				if flag > 0:
					count += 1
					break
		#print count
		jaccard = float(count)/float(l_sogou+l_baidu-count)
		return jaccard

	def Kendall(self, baiduSERP,sogouSERP):
		count = 0
		l_baidu = len(baiduSERP)
		l_sogou = len(sogouSERP)
		similar_list = []
		for i in range(0, l_baidu):
			for j in range(0, l_sogou):
				flag = self.urlSimilar(self.cleanurl(baiduSERP[i]),self.cleanurl(sogouSERP[j].url))
				if flag:
					if j not in similar_list:
						similar_list.append(j)

		for i in range(0, len(similar_list)):
			for j in range(i+1, len(similar_list)):
				if similar_list[i] < similar_list[j]:
					count += 1
		#print len(similar_list)
		tau = float(count)*2/float(l_baidu*(l_baidu-1))
		return tau

def compute_Jaccard(baiduSERP, sogouSERP):
    return url().urlJaccard(baiduSERP, sogouSERP)

def compute_Kendall(baiduSERP, sogouSERP):
    return url().Kendall(baiduSERP, sogouSERP)

sogou = ParseSogou()
baidu = ParseBaidu()
sogouSERPs = sogou.getResults(1, 11, 10, "./query.txt", "./SERP_sogou/")
baiduSERPs = baidu.getResults(1, 11, 10, "./query.txt", "./SERP_baidu/")
for i in range(0, len(sogouSERPs)):
    print 'query: ' + sogouSERPs[i][0].query + 'Jaccard: ' + str(compute_Jaccard(baiduSERPs[i], sogouSERPs[i]))
    print 'query: ' + sogouSERPs[i][0].query + 'Kendall: ' + str(compute_Kendall(baiduSERPs[i], sogouSERPs[i]))

