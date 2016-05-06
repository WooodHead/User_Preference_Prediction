#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

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

    # vertical specific category
    vertical_category = {}
    encyclopedia = 0
    gps_map = 0
    forum = 0
    download = 0
    image = 0
    image_text = 0
    video = 0
    news = 0
    experience = 0
    reading = 0
    others = 0

    def __init__(self, qid, query, rank, title, snippet, url, vertical, figure, vertical_dictionary):
        self.qid = qid
        self.query = query
        self.rank = rank
        self.title = title
        self.snippet = snippet
        self.url = url
        self.vertical = vertical
        self.figure = figure
        self.update_vertical_dictionary(vertical_dictionary)

    def update_vertical_dictionary(self, vertical_dictionary):
        category = ["encyclopedia", "gps_map", "forum", "download", "image", "image_text", "video", "news", "experience", "reading", "others"]
        if vertical_dictionary['encyclopedia'] == 1:
            self.encyclopedia = 1
            self.vertical = 1
        else:
            self.encyclopedia = 0
        if vertical_dictionary['gps_map'] == 1:
            self.gps_map = 1
            self.vertical = 1
        else:
            self.gps_map = 0
        if vertical_dictionary['forum'] == 1:
            self.forum = 1
            self.vertical = 0
        else:
            self.forum = 0
        if vertical_dictionary['download'] == 1:
            self.download = 1
            self.vertical = 1
        else:
            self.download = 0
        if vertical_dictionary['image'] == 1:
            self.image = 1
            self.vertical = 1
        else:
            self.image = 0
        if vertical_dictionary['image_text'] == 1:
            self.image_text = 1
            self.vertical = 1
        else:
            self.image_text = 0
        if vertical_dictionary['video'] == 1:
            self.video = 1
            self.vertical = 1
        else:
            self.video = 0
        if vertical_dictionary['news'] == 1:
            self.news = 1
            self.vertical = 0
        else:
            self.news = 0
        if vertical_dictionary['experience'] == 1:
            self.experience = 1
            self.vertical = 1
        else:
            self.experience = 0
        if vertical_dictionary['reading'] == 1:
            self.reading = 1
            self.vertical = 1
        else:
            self.reading = 0
        if vertical_dictionary['others'] == 1:
            self.others = 1
            self.vertical = 1
        else:
            self.others = 0

    def Print(self):
        print str(self.qid)+"\t" + self.query + "\t" + str(self.rank) + "\t" + self.title.strip() + "\t" + self.snippet.strip() + '\t' + self.url + "\tfigure? " + str(self.figure)

    def output_category(self):
        category_name = ["encyclopedia", "gps_map", "forum", "download", "image", "image_text", "video", "news", "experience", "reading", "others"]
        for i in range(len(category_name)):
            print category_name[i]+": "+str(eval(str("self.")+str(category_name[i])))+",",
        print "\n"


class ParseSogou:

    def getResults(self, start_a, end_b, windows, query_file_path, page_folder_path):

        result_list = []
        # queries_lines = open("../Files/query_id.txt","r").readlines()
        queries_lines = open(query_file_path, "r").readlines()
        queries = ["index"]
        # start from 1
        for query in queries_lines:
            query = query.strip()
            queries.append(query)

        for i in range(start_a, end_b):  # the range of query
            if i >= len(queries):
                break
            query = queries[i]
            file_path = page_folder_path + query + '_sogou.html'
            try:
                fin = open(file_path, 'r')
                fin.close()
            except:
                continue

            # print file_path
            print "Sogou " + query, i
            Results = []
            count = 0
            p = Parser()
            resultlists = p.parseSERP(file_path)
            for item in resultlists:
                count += 1

                title = item.title
                url = item.mainurl
                # print str(item.figure) +"\t" + item.title

                if "title" in item.resulttype:
                    # print item.figure
                    vertical = 1
                else:
                    vertical = 0
                if vertical:
                    snippet = item.othertext
                else:
                    snippet = item.summary

                result = SearchResult(i,query,count,title,snippet,url,vertical,item.figure,item.vertical_dictionary)
                Results.append(result)
                if count == windows:
                    break
            # print query

            result_list.append(Results)

        return result_list

if __name__ == '__main__':
    l = ParseSogou()
    resultlist  = l.getResults(1, 2088, 10, "../data/query.txt", "../../annotation_platform/static/SERP_sogou/")
    fout = open('../data/sogou_results_info.txt', 'w')
    fout.write('query\trank\ttitle\tsnippet\tmainurl\tverticaltype\n')
    for Results in resultlist:
        for item in Results:
            item.Print()
            item.output_category()

            vertical_type = 'organic'
            category_name = ["encyclopedia", "gps_map", "forum", "download", "image", "image_text", "video", "news", "experience", "reading", "others"]
            for i in range(len(category_name)):
                if str(eval(str("item.")+str(category_name[i]))) == '1':
                    vertical_type = category_name[i]
            fout.write(item.query + "\t" + str(item.rank) + "\t" + item.title.strip() + "\t" + item.snippet.strip() + '\t' + item.url + '\t' + vertical_type)
            fout.write('\n')
    fout.close()
