#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'
from selenium import webdriver
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Position:
    def __init__(self, type_, qid, query, rank, left, top, width, height):
        self.type_ = type_
        self.qid = qid
        self.query = query
        self.rank = rank
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def Print(self):
        print str(self.type_) + "\t" + str(self.qid)+"\t" + self.query + "\t" + str(self.rank) + "\t" + "(" + str(self.left) + "," + str(self.top) + ")\t" + "(" + str(self.width) + "," + str(self.height) + ")"

    def output(self):
        return [self.query, str(self.rank), str(self.left), str(self.top), str(self.width), str(self.height)]


class ParseSogouPosition:
    def get_positon(self, start_a, end_b, windows, query_file_path, page_folder_path):
        results_position_list = []
        images_position_list = []
        queries_lines = open(query_file_path, "r").readlines()
        queries = ["index"]
        # start from 1
        for query in queries_lines:
            query = query.strip()
            queries.append(query)

        driver = webdriver.PhantomJS()
        for i in range(start_a, end_b):  # the range of query
            if i >= len(queries):
                break
            query = queries[i]
            file_path = page_folder_path + query + '_sogou.html'
            code_file_path = page_folder_path + urllib2.quote(query, '+') + '_sogou.html'
            try:
                fin = open(file_path, 'r')
                fin.close()
            except:
                continue

            try:
                Results_position = []
                Images_position = []
                count = 0
                driver.get(code_file_path)
                content_results = driver.find_element_by_id('main')
                divs = content_results.find_elements_by_css_selector('div')
                for div in divs:
                    classes = div.get_attribute('class').split(' ')
                    if 'rb' in classes or 'vrwrap' in classes:
                        count += 1
                        result_position = Position("query", i, query, count, div.location['x'], div.location['y'], div.size['width'], div.size['height'])
                        Results_position.append(result_position)
                        # anchors = div.find_elements_by_css_selector("a")
                        images = div.find_elements_by_css_selector("img")
                        Images = []
                        for image in images:
                            image = image.find_element_by_xpath('..')
                            if image.size['width'] == 0 or image.size['height'] == 0:
                                continue
                            image_position = Position("image", i, query, count, image.location['x'], image.location['y'], image.size['width'], image.size['height'])
                            Images.append(image_position)
                        Images_position.append(Images)
                        if count == windows:
                            break
                results_position_list.append(Results_position)
                images_position_list.append(Images_position)
                print "Sogou " + query, i
            except:
                continue

        driver.quit()
        return results_position_list, images_position_list


if __name__ == '__main__':
    l = ParseSogouPosition()
    results_position_list, images_position_list = l.get_positon(1, 2088, 10, "../data/query.txt", "../../annotation_platform/static/SERP_sogou/")
    fout = open('../data/sogou_results_position.txt', 'w')
    fout.write('query\trank\tleft\ttop\twidth\theight\n')
    for Results in results_position_list:
        for item in Results:
            item.Print()
            fout.write('\t'.join(item.output()))
            fout.write('\n')
    fout.close()

    fout = open('../data/sogou_images_position.txt', 'w')
    fout.write('query\trank\tleft\ttop\twidth\theight\n')
    for Images in images_position_list:
        for images in Images:
            for item in images:
                item.Print()
                fout.write('\t'.join(item.output()))
                fout.write('\n')
    fout.close()
