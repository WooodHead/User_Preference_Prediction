#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup
import traceback
import time

def clean_url(url):
	part = url.split("/")
	length = len(part)
	#print length
	if length !="1":
		url = url.replace(part[length-1],"")
	return url

class SearchResult:
	title = ""
	snippet = ""
	url = ""
	query = ""
	qid = 0
	figure = 0
	vertical = 0
	coverage = 0.0
	Similarity = 0.0
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

	def __init__(self, qid,  query, rank, title,snippet, url, vertical,figure,vertical_dictionary):
		self.qid = qid
		self.query = query
		self.rank= rank
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
			vertical = 1
		else:
			encyclopedia = 0
		if vertical_dictionary['download'] == 1:
			self.download = 1
			vertical = 1
		else:
			download = 0
		if vertical_dictionary['video'] == 1:
			self.video = 1
			vertical = 1
		else:
			video = 0
		if vertical_dictionary['stock'] == 1:
			self.stock = 1
			vertical = 1
		else:
			stock = 0
		if vertical_dictionary['news'] == 1:
			self.news = 1
			vertical = 1
		else:
			news = 0
		if vertical_dictionary['forum'] == 1:
			self.forum= 1
			vertical = 1
		else:
			forum = 0
		if vertical_dictionary['experience'] == 1:
			self.experience = 1
			vertical = 1
		else:
			experience= 0
		if vertical_dictionary['reading'] == 1:
			self.reading = 1
			vertical = 1
		else:
			reading= 0
		if vertical_dictionary['gps_map'] == 1:
			self.gps_map = 1
			vertical = 1
		else:
			gps_map= 0

	def Print(self):
		print str(self.qid)+"\t" + self.query + "\t"+ str(self.rank) + "\t" + self.title.encode("utf8") + "\t figure? " + str(self.figure)
		#print

	def Geturl(self):
		return self.url

	def output_category(self):
		category_name = ["encyclopedia","download","video","stock","news","forum","experience","reading","gps_map"]
		for i in range(len(category_name)):
			print category_name[i]+": "+str(eval(str("self.")+str(category_name[i])))+",",
		print "\n"


class ParseBaidu:

	def get_vertical_dictionary(self,child):
		vertical_dictionary = {}

		# op-sotckdynamic for stock
		if child.find_all("div",class_ = "op-sotckdynamic"):
			vertical_dictionary["stock"] = 1
			#print "stock"
		else:
			vertical_dictionary["stock"] = 0

		#(op-soft-container with div )for downloading (c-icon c-gap-right-small with i)
		#if child.find_all("div",class_ = "op-soft-container") or child.find_all("i",class_= "c-icon-download-noborder"):
		if child.find_all("i",class_= "c-icon-download-noborder") or child["tpl"] == "soft":
			vertical_dictionary["download"] = 1
			#print "soft"
		else:
			vertical_dictionary["download"] = 0

		#op-bk-polysemy-album with "a" for encyclopedia
		#if child.find_all("a",class_ = "op-bk-polysemy-album"):
		if child["tpl"] == "bk_polysemy":
			vertical_dictionary["encyclopedia"] = 1
			#print "baike"
		else:
			vertical_dictionary["encyclopedia"] = 0

		# st_com_abstract_novelicon with "i" for reading
		if child.find_all("i",class_ = "st_com_abstract_novelicon"):
			vertical_dictionary["reading"] = 1
			#print "reading"
		else:
			vertical_dictionary["reading"] = 0
		## news with tpl of sp_realtime or
		if child["tpl"] == "sp_realtime":
			vertical_dictionary["news"] = 1
			#print "news"
		else:
			vertical_dictionary["news"] = 0

		## tpl of "jingyan_summary" for Baidu Jingyan:
		if child["tpl"] == "jingyan_summary":
			vertical_dictionary["experience"] = 1
			#print "jingyan"
		else:
			vertical_dictionary["experience"] = 0

		## tplf of "tieba" for forum:
		if child["tpl"] == "tieba":
			vertical_dictionary["forum"] = 1
			#print "tieba"
		else:
			vertical_dictionary["forum"] = 0
		## tpl of "se_st_single_video_zhanzhang" or "vd_mininewest"
		if child["tpl"] == "vd_mininewest" or child["tpl"] == "se_st_single_video_zhanzhang" or child["tpl"] == "zx_new_tvideo":
			vertical_dictionary["video"] = 1
			#print "video"
		else:
			vertical_dictionary["video"] = 0


		if child["tpl"] == "mapdots" :
			vertical_dictionary["gps_map"] = 1
		else:
			vertical_dictionary["gps_map"] = 0

		return vertical_dictionary


	def getResults(self,start_a,end_b,windows,query_file_path,page_folder_path):
		# threshold is top t result
		result_list = []
		urllists = []
		#queries_lines = open("../Files/query_id.txt","r").readlines()
		queries_lines = open(query_file_path,"r").readlines()
		queries = ["index"] # start from 1
		for query in queries_lines:
			query = query.strip()
			queries.append(query)

		for i in range(start_a,end_b):
			urllist = []
			#file_path = "../Baidu/"+queries[i]
			file_path = page_folder_path + queries[i] + '_baidu.html'
			#print file_path
			query = queries[i]
			soup = BeautifulSoup(open(file_path,"r").read())
			container_l = soup.find_all("div", id = "content_left")[0]
			count = 0
			Results = []
			flag = 0
			print "Baidu\t" + query

			for child in container_l.children:
				figure = 0
				count += 1
				url = ''
				try:
					if "result-op" in child["class"]:
						vertical = 1
					else:
						vertical = 0
					#print "class attributes are " + child["tpl"]

					img = child.find_all("img")

					if len(img)!=0:
						figure = 1
					#try:
					title = child.find_all("h3")
					#except:
					#	title = child.find_all("div",class_="op-soft-title")[0]
					#
					if not vertical:

						snippet = 	child.find_all("div", class_ = "c-abstract")[0]
						snippet = snippet.get_text()
						if len(title) > 0:

							for h3node in title:
								for item in h3node.children:
									if item.name == 'a':

										if 'href' in item.attrs:

											url = item['href']

					else:
						#try:
						#	snippet = child.find_all("div", class_ ="c-border")[0]
						#except:
						#	snippet = child.find_all("div", class_ ="c-row")[0]
						#snippet = snippet.get_text().strip().replace("\n","")[:140]
						snippet = ""
						url = child.find_all("span", class_= "c-showurl")[0].get_text()

					vertical_dictionary = {}
					urllist.append(url)
					result = SearchResult(i,query,count,title,snippet,url,vertical,figure,vertical_dictionary)
					print 'hh'
					Results.append(result)


				except:
					count = count - 1
					#print "sth is wrong"
					#traceback.print_exc()
				if count > windows:
					#print "Windows Ends"
					break
			urllists.append(urllist)
			result_list.append(Results)

		return urllists

if __name__ == '__main__':
	p = ParseBaidu()
	urllists  = p.getResults(1, 11, 10, "./query.txt", "./SERP_baidu/")
	for urllist in urllists:
		for item in urllist:
			print item
	time.sleep(5)
