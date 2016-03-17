#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup
from SERPExtractor import Parser

class SearchResult:
	title = ""
	snippet = ""
	url = ""
	query = ""
	qid = 0
	vertical = 0.0
	coverage = 0.0
	Similarity = 0.0
	figure = 0
	rank = 0

	## vertical specific category
	vertical_category = {}
	encyclopedia = 0
	download = 0
	video = 0
	stock = 0 
	news = 0
	forum = 0
	experience = 0
	reading = 0
	gps_map = 0
	
	def __init__(self,qid, query, rank, title,snippet, url, vertical,figure,vertical_dictionary):
		self.qid = qid
		self.query = query
		self.rank = rank
		self.title = title
		self.snippet = snippet
		self.url = url
		self.vertical = vertical
		self.figure = figure
		self.update_vertical_dictionary(vertical_dictionary)

	def update_vertical_dictionary(self,vertical_dictionary):
		category = ["encyclopedia","download","video","stock","news","forum","experience","reading","gps_map"]
		if vertical_dictionary['encyclopedia'] == 1:
			self.encyclopedia = 1
			self.vertical = 1
		else:
			encyclopedia = 0
		if vertical_dictionary['download'] == 1:
			self.download = 1
			self.vertical = 1
		else:
			download = 0
		if vertical_dictionary['video'] == 1:
			self.video = 1
			self.vertical = 1
		else:
			video = 0
		if vertical_dictionary['stock'] == 1:
			self.stock = 1
			self.vertical = 1
		else:
			stock = 0
		if vertical_dictionary['news'] == 1:
			self.news = 1
			self.vertical = 0
		else:
			news = 0
		if vertical_dictionary['forum'] == 1:
			self.forum= 1
			self.vertical = 0
		else:
			forum = 0
		if vertical_dictionary['experience'] == 1:
			self.experience = 1
			self.vertical = 1
		else:
			experience= 0
		if vertical_dictionary['reading'] == 1:
			self.reading = 1
			self.vertical = 1
		else:
			reading= 0	
		if vertical_dictionary['gps_map'] == 1:
			self.gps_map = 1
			self.vertical = 1
		else:
			gps_map= 0

	def Print(self):
		print str(self.qid)+"\t" + self.query + "\t"+ str(self.rank) + "\t" + self.title + "\t figure? " + str(self.figure)

	def Geturl(self):
		return self.url
	
	def output_category(self):
		category_name = ["encyclopedia","download","video","stock","news","forum","experience","reading","gps_map"]
		for i in range(len(category_name)):
			print category_name[i]+": "+str(eval(str("self.")+str(category_name[i])))+",",
		print "\n"

class ParseSogou:

	def getResults(self,start_a,end_b,windows,query_file_path,page_folder_path):

		result_list = []
		#queries_lines = open("../Files/query_id.txt","r").readlines()
		queries_lines = open(query_file_path,"r").readlines()
		queries = ["index"]
		# start from 1
		for query in queries_lines:
			query = query.strip()
			queries.append(query)

		for i in range(start_a,end_b): # the range of query
			#file_path = "../Sogou/"+queries[i]
			file_path = page_folder_path + queries[i] + '_sogou.html'
			#print file_path
			query = queries[i]
			print "Sogou " + query
			Results = []
			count = 0
			p = Parser()
			resultlists = p.parseSERP(file_path)
			for item in resultlists:
				count += 1

				title = item.title
				url  = item.mainurl
				#print str(item.figure) +"\t" + item.title

				if "title" in item.resulttype:
					#print item.figure
					vertical = 1
				else:
					vertical = 0
				if vertical:
					snippet = item.othertext
				else:
					snippet = item.summary

				result = SearchResult(i,query,count,title,snippet,url,vertical,item.figure,item.vertical_dictionary)
				Results.append(result)
				if count > windows:
					break
			#print query

			result_list.append(Results)

		return result_list

if __name__=='__main__':
	l = ParseSogou()
	resultlist  = l.getResults(1, 11, 10, "./query.txt", "./SERP_sogou/")
	for Result in resultlist:
		for item in Result:
			print item.Geturl()