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


class ParseBaiduPosition:
    def get_positon(self, start_a, end_b, windows, query_file_path, page_folder_path):
        results_position_list = []
        images_position_list = []
        queries_lines = open(query_file_path, "r").readlines()
        queries = ["index"]
        # start from 1
        for query in queries_lines:
            query = query.strip()
            queries.append(query)

        for i in range(start_a, end_b):  # the range of query
            # file_path = "../Baidu/"+queries[i]
            query = queries[i]
            file_path = page_folder_path + query + '_baidu.html'
            code_file_path = page_folder_path + urllib2.quote(query, '+') + '_baidu.html'
            try:
                fin = open(file_path, 'r')
                fin.close()
            except:
                continue

            try:
                Results_position = []
                Images_position = []
                count = 0
                driver = webdriver.PhantomJS()
                driver.get(code_file_path)
                content_l = driver.find_element_by_id('content_left')
                containers = content_l.find_elements_by_css_selector("div[class~=c-container]")
                for container in containers:
                    count += 1
                    result_position = Position("query", i, query, count, container.location['x'], container.location['y'], container.size['width'], container.size['height'])
                    Results_position.append(result_position)
                    images = container.find_elements_by_css_selector("img")
                    Images = []
                    for image in images:
                        image_position = Position("image", i, query, count, image.location['x'], image.location['y'], image.size['width'], image.size['height'])
                        Images.append(image_position)
                    Images_position.append(Images)
                    if count == windows:
                        break
                driver.quit()
                results_position_list.append(Results_position)
                images_position_list.append(Images_position)
                print "Baidu " + query
            except:
                continue

        return results_position_list, images_position_list


if __name__ == '__main__':
    l = ParseBaiduPosition()
    results_position_list, images_position_list = l.get_positon(1, 3, 10, "../data/query.txt", "/Users/franky/undergraduate/courses/graduation_project/annotation_platform/static/SERP_baidu/")
    for Results in results_position_list:
        for item in Results:
            item.Print()
    for Images in images_position_list:
        for images in Images:
            for item in images:
                item.Print()
