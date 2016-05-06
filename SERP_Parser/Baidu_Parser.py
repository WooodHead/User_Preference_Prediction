#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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


class ParseBaidu:

    def get_vertical_dictionary(self, child, image_text, vertical):
        vertical_dictionary = {}

        if "bk" in child["tpl"]:
            vertical_dictionary["encyclopedia"] = 1
        else:
            vertical_dictionary["encyclopedia"] = 0

        if "map" in child["tpl"]:
            vertical_dictionary["gps_map"] = 1
        else:
            vertical_dictionary["gps_map"] = 0

        if "qa" in child["tpl"] or "tieba" in child["tpl"] or child['srcid'] == '1529' or child['srcid'] == '1528' or child['srcid'] == '1533':
            vertical_dictionary["forum"] = 1
        else:
            vertical_dictionary["forum"] = 0

        if child.select("i[class~=c-icon-download-noborder]") or child["tpl"] == "soft":
            vertical_dictionary["download"] = 1
        else:
            vertical_dictionary["download"] = 0

        if "img" in child["tpl"]:
            vertical_dictionary["image"] = 1
        else:
            vertical_dictionary["image"] = 0

        if image_text:
            vertical_dictionary["image_text"] = 1
        else:
            vertical_dictionary["image_text"] = 0

        if child["tpl"] == "vd_mininewest" or "tvideo" in child["tpl"] or "single_video" in child["tpl"]:
            vertical_dictionary["video"] = 1
        else:
            vertical_dictionary["video"] = 0

        if "sp_realtime" in child["tpl"]:
            vertical_dictionary["news"] = 1
        else:
            vertical_dictionary["news"] = 0

        if child["srcid"] == '1526' or child["srcid"] == '1525':
            vertical_dictionary["reading"] = 1
        else:
            vertical_dictionary["reading"] = 0

        if "jingyan" in child["tpl"]:
            vertical_dictionary["experience"] = 1
        else:
            vertical_dictionary["experience"] = 0

        if vertical:
            flag = True
            for category in ["encyclopedia", "gps_map", "forum", "download", "image", "image_text", "video", "news", "experience", "reading"]:
                if vertical_dictionary[category] == 1:
                    flag = False
                    break
            if flag:
                vertical_dictionary["others"] = 1
            else:
                vertical_dictionary["others"] = 0
        else:
            vertical_dictionary["others"] = 0

        return vertical_dictionary

    def getResults(self, start_a, end_b, windows, query_file_path, page_folder_path):

        result_list = []
        # queries_lines = open("../Files/query_id.txt","r").readlines()
        queries_lines = open(query_file_path, "r").readlines()
        queries = ["index"]
        # start from 1
        for query in queries_lines:
            query = query.strip()
            queries.append(query)

        for i in range(start_a, end_b):
            if i >= len(queries):
                break
            query = queries[i]
            file_path = page_folder_path + query + '_baidu.html'
            try:
                fin = open(file_path, 'r')
                fin.close()
            except:
                continue

            soup = BeautifulSoup(open(file_path, "r").read())
            try:
                container_l = soup.find_all("div", id="content_left")[0]
            except:
                continue

            count = 0
            Results = []
            # print file_path
            print "Baidu " + query, i
            flag = 0

            for child in container_l.children:
                figure = 0
                count += 1
                vertical = 0
                image_text = False
                try:
                    if child["srcid"] != "1599":
                        vertical = 1
                    else:
                        for div in child.children:
                            if u'class' in div.attrs:
                                if "c-row" in div['class']:
                                    vertical = 1
                                    image_text = True
                                    break
                                else:
                                    vertical = 0
                    # print "class attributes are " + child["tpl"]

                    img = child.find_all("img")

                    if len(img) != 0:
                        figure = 1
                    # try:
                    h3node = child.find_all("h3")[0]
                    title = ''
                    for line in h3node.get_text().split('\n'):
                        if line.strip() != '':
                                title += line.strip()+' '
                    anchor = h3node.find_all("a")[0]
                    url = anchor['href']

                    # except:
                    #     title = child.find_all("div",class_="op-soft-title")[0]
                    #
                    abstracts = child.find_all("div", class_="c-abstract")
                    if len(abstracts) > 0:
                        abstract = abstracts[0]
                        snippet = abstract.get_text(strip=True)
                    else:
                        abstracts = child.select("div[class~=c-span18]")
                        if len(abstracts) > 0:
                            abstract = abstracts[0]
                            snippet = abstract.get_text(strip=True)
                        else:
                            snippet = ""

                    vertical_dictionary = self.get_vertical_dictionary(child, image_text, vertical)
                    result = SearchResult(i, query, count, title, snippet, url, vertical, figure, vertical_dictionary)

                    Results.append(result)


                except:
                    count -= 1
                    # print "sth is wrong"
                    # traceback.print_exc()
                if count == windows:
                    # print "Windows Ends"
                    break

            result_list.append(Results)
        return result_list

if __name__ == "__main__":
    l = ParseBaidu()
    resultlist  = l.getResults(1, 2088, 10, "../data/query.txt", "../../annotation_platform/static/SERP_baidu/")
    fout = open('../data/baidu_results_info.txt', 'w')
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
