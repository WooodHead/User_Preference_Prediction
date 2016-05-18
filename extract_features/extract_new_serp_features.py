#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'
from collections import defaultdict
import jieba
import numpy as np
from selenium import webdriver
import urllib2
from bs4 import BeautifulSoup


def extract_url_features(baidu_results, sogou_results):
    baidu_identical_urls = {}
    sogou_identical_urls = {}

    #if len(baidu_results) != len(sogou_results):
     #   return None
    # 由于url的编码问题,尝试过几种打开url重定向的方法,效果都不是很好...干脆选择比较title的方法
    try:
        baidu_landing_pages_title = {}
        sogou_landing_pages_title = {}
        for rank in baidu_results.keys():
            title = baidu_results[rank]['item3']
            baidu_landing_pages_title[rank] = title
        for rank in sogou_results.keys():
            title = sogou_results[rank]['item3']
            sogou_landing_pages_title[rank] = title
        for rank_baidu in baidu_landing_pages_title.keys():
            baidu_title = baidu_landing_pages_title[rank_baidu]
            if baidu_title == '' or '百科' in baidu_title:
                baidu_identical_urls[rank_baidu] = 0
            else:
                for rank_sogou in sogou_landing_pages_title.keys():
                    if rank_sogou in sogou_identical_urls.keys():
                        continue
                    sogou_title = sogou_landing_pages_title[rank_sogou]
                    if sogou_title == '':
                        sogou_identical_urls[rank_sogou] = 0
                        continue
                    if baidu_title == sogou_title:
                        baidu_identical_urls[rank_baidu] = 1
                        sogou_identical_urls[rank_sogou] = 1
                        break
                if rank_baidu not in baidu_identical_urls.keys():
                    baidu_identical_urls[rank_baidu] = 0
        for rank_sogou in sogou_landing_pages_title.keys():
            if rank_sogou not in sogou_identical_urls.keys():
                sogou_identical_urls[rank_sogou] = 0

        '''for rank in baidu_results.keys():
            raw_url = baidu_results[rank]['item5']
            try:
                req_timeout = 5
                header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
                req = urllib2.Request(raw_url, None, header)
                resp = urllib2.urlopen(req, None, req_timeout)
                url = resp.geturl()

            except:
                url = raw_url
            baidu_urls[rank] = url

        for rank in sogou_results.keys():
            raw_url = sogou_results[rank]['item5']
            try:
                req_timeout = 5
                header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
                req = urllib2.Request(raw_url, None, header)
                resp = urllib2.urlopen(req, None, req_timeout)
                url = resp.geturl()

            except:
                url = raw_url
            sogou_urls[rank] = url'''
        return [baidu_identical_urls, sogou_identical_urls]
    except:
        return None


def extract_result_features(query, results, results_position, images_position, identical_urls):
    category_name = {"":0, "encyclopedia":1, "gps_map":2, "forum":3, "download":4, "image":5, "image_text":6, "video":7, "news":8, "experience":9, "reading":10, "others":11}

    features = {}

    first_screen_end = 11
    title_char_length_list = []
    title_word_length_list = []
    title_matches_fraction_with_query_list = []
    snippet_char_length_list = []
    snippet_word_length_list = []
    snippet_matches_fraction_with_query_list = []
    rank_of_the_first_vertical_result = 0
    position_y_of_the_first_vertical_result = -1
    height_of_the_first_vertical_result = 0
    rank_of_the_first_result_with_image = 0
    position_y_of_the_first_result_with_image = -1
    height_of_the_first_result_with_image = 0
    for rank in range(1, 11):
        if rank in results.keys() and rank in results_position.keys():
            title = results[rank]['item3']
            snippet = results[rank]['item4']
            vertical_type = results[rank]['item6']
            result_left = float(results_position[rank]['item3'])
            result_top = float(results_position[rank]['item4'])
            result_width = float(results_position[rank]['item5'])
            result_height = float(results_position[rank]['item6'])

            title_char_length = len(title)
            title_seg_list = jieba.lcut(title, cut_all=False)
            title_word_length = 0
            for item in title_seg_list:
                title_word_length += 1
            snippet_char_length = len(snippet)
            snippet_seg_list = jieba.lcut(snippet, cut_all=False)
            snippet_word_length = 0
            for item in snippet_seg_list:
                snippet_word_length += 1
            title_matches = 0
            snippet_matches = 0
            query_seg_list = jieba.lcut(query, cut_all=False)
            for query_item in query_seg_list:
                for item in title_seg_list:
                    if query_item == item:
                        title_matches += 1
                for item in snippet_seg_list:
                    if query_item == item:
                        snippet_matches += 1
            title_char_length_list.append(title_char_length)
            title_word_length_list.append(title_word_length)
            if title_matches:
                title_matches_fraction_with_query_list.append(float(title_matches) / title_word_length)
            else:
                title_matches_fraction_with_query_list.append(0)
            snippet_char_length_list.append(snippet_char_length)
            snippet_word_length_list.append(snippet_word_length)
            if snippet_matches:
                snippet_matches_fraction_with_query_list.append(float(snippet_matches) /snippet_word_length)
            else:
                snippet_matches_fraction_with_query_list.append(0)

            if first_screen_end == 11:
                if result_top + result_height / 2 > 600:
                    first_screen_end = rank

            if rank_of_the_first_vertical_result == 0:
                if vertical_type != 'organic':
                    rank_of_the_first_vertical_result = rank
                    position_y_of_the_first_vertical_result = result_top
                    height_of_the_first_vertical_result = result_height
            if rank_of_the_first_result_with_image == 0:
                if rank in images_position.keys():
                    for each_image in images_position[rank]:
                        left, top, width, height = each_image
                        left = float(left)
                        top = float(top)
                        width = float(width)
                        height = float(height)
                        right = left + width
                        bottom = top + height
                        is_displayed = True
                        result_right = result_left + result_width
                        result_bottom = result_top + result_height
                        if left < result_left or right > result_right or top < result_top or bottom > result_bottom:
                            is_displayed = False
                        if is_displayed:
                            rank_of_the_first_result_with_image = rank
                            position_y_of_the_first_result_with_image = result_top
                            height_of_the_first_result_with_image = result_height
                            break

    if rank_of_the_first_vertical_result:
        features['reciprocal_of_the_rank_of_the_first_vertical_result'] = 1.0 / rank_of_the_first_vertical_result
    else:
        features['reciprocal_of_the_rank_of_the_first_vertical_result'] = 0
    features['position_y_of_the_first_vertical_result'] = position_y_of_the_first_vertical_result
    features['height_of_the_first_vertical_result'] = height_of_the_first_vertical_result
    if rank_of_the_first_result_with_image:
        features['reciprocal_of_the_rank_of_the_first_result_with_image'] = 1.0 / rank_of_the_first_result_with_image
    else:
        features['reciprocal_of_the_rank_of_the_first_result_with_image'] = 0
    features['position_y_of_the_first_result_with_image'] = position_y_of_the_first_result_with_image
    features['height_of_the_first_result_with_image'] = height_of_the_first_result_with_image

    try:
        features['max_title_char_length_first_screen'] = np.max(title_char_length_list[:first_screen_end-1])
        features['max_title_char_length_other_screens'] = np.max(title_char_length_list[first_screen_end-1:])
        features['avg_title_char_length_first_screen'] = np.mean(title_char_length_list[:first_screen_end-1])
        features['avg_title_char_length_other_screens'] = np.mean(title_char_length_list[first_screen_end-1:])
        features['max_title_word_length_first_screen'] = np.max(title_word_length_list[:first_screen_end-1])
        features['max_title_word_length_other_screens'] = np.max(title_word_length_list[first_screen_end-1:])
        features['avg_title_word_length_first_screen'] = np.mean(title_word_length_list[:first_screen_end-1])
        features['avg_title_word_length_other_screens'] = np.mean(title_word_length_list[first_screen_end-1:])
        features['max_title_matches_fraction_with_query_first_screen'] = np.max(title_matches_fraction_with_query_list[:first_screen_end-1])
        features['max_title_matches_fraction_with_query_other_screens'] = np.max(title_matches_fraction_with_query_list[first_screen_end-1:])
        features['avg_title_matches_fraction_with_query_first_screen'] = np.mean(title_matches_fraction_with_query_list[:first_screen_end-1])
        features['avg_title_matches_fraction_with_query_other_screens'] = np.mean(title_matches_fraction_with_query_list[first_screen_end-1:])
        features['max_snippet_char_length_first_screen'] = np.max(snippet_char_length_list[:first_screen_end-1])
        features['max_snippet_char_length_other_screens'] = np.max(snippet_char_length_list[first_screen_end-1:])
        features['avg_snippet_char_length_first_screen'] = np.mean(snippet_char_length_list[:first_screen_end-1])
        features['avg_snippet_char_length_other_screens'] = np.mean(snippet_char_length_list[first_screen_end-1:])
        features['max_snippet_word_length_first_screen'] = np.max(snippet_word_length_list[:first_screen_end-1])
        features['max_snippet_word_length_other_screens'] = np.max(snippet_word_length_list[first_screen_end-1:])
        features['avg_snippet_word_length_first_screen'] = np.mean(snippet_word_length_list[:first_screen_end-1])
        features['avg_snippet_word_length_other_screens'] = np.mean(snippet_word_length_list[first_screen_end-1:])
        features['max_snippet_matches_fraction_with_query_first_screen'] = np.max(snippet_matches_fraction_with_query_list[:first_screen_end-1])
        features['max_snippet_matches_fraction_with_query_other_screens'] = np.max(snippet_matches_fraction_with_query_list[first_screen_end-1:])
        features['avg_snippet_matches_fraction_with_query_first_screen'] = np.mean(snippet_matches_fraction_with_query_list[:first_screen_end-1])
        features['avg_snippet_matches_fraction_with_query_other_screens'] = np.mean(snippet_matches_fraction_with_query_list[first_screen_end-1:])
    except:
        return None

    # url features
    first_identical_url = 0
    rank_of_the_identical_urls = []
    for rank in range(1, 11):
        if rank in identical_urls.keys():
            if identical_urls[rank]:
                if not first_identical_url:
                    first_identical_url = rank
                rank_of_the_identical_urls.append(rank)
    average_of_reciprocal_of_the_rank_of_the_identical_urls = 0
    if len(rank_of_the_identical_urls) > 0:
        reciprocal_sum = 0
        for rank in rank_of_the_identical_urls:
            reciprocal_sum += 1.0 / rank
        average_of_reciprocal_of_the_rank_of_the_identical_urls = reciprocal_sum / len(rank_of_the_identical_urls)
    if first_identical_url:
        features['reciprocal_of_the_rank_of_the_first_identical_url'] = 1.0 / first_identical_url
    else:
        features['reciprocal_of_the_rank_of_the_first_identical_url'] = 0.0
    features['average_of_reciprocal_of_the_rank_of_the_identical_urls'] = average_of_reciprocal_of_the_rank_of_the_identical_urls

    number_identical_urls = 0.0
    number_urls = 0.0
    had_identical_url = 0
    for rank in range(1, first_screen_end):
        if rank in identical_urls.keys():
            number_urls += 1
            if identical_urls[rank] == 1:
                number_identical_urls += 1
                had_identical_url = 1
    if number_identical_urls:
        features['fraction_of_identical_urls_first_screen'] = number_identical_urls / number_urls
    else:
        features['fraction_of_identical_urls_first_screen'] = 0.0
    features['had_identical_url_first_screen'] = had_identical_url

    number_identical_urls = 0.0
    number_urls = 0.0
    had_identical_url = 0
    for rank in range(first_screen_end, 11):
        if rank in identical_urls.keys():
            number_urls += 1
            if identical_urls[rank] == 1:
                number_identical_urls += 1
                had_identical_url = 1
    if number_identical_urls:
        features['fraction_of_identical_urls_other_screens'] = number_identical_urls / number_urls
    else:
        features['fraction_of_identical_urls_other_screens'] = 0.0
    features['had_identical_url_other_screens'] = had_identical_url

    number_vertical_results = 0.0
    number_results_with_images = 0.0
    number_images = 0.0
    number_results = 0.0
    total_height = 0.0
    total_width = 0.0
    total_vertical_results_height = 0.0
    total_results_with_images_height = 0.0
    total_images_area = 0.0
    vertical_types = []
    for rank in range(1, first_screen_end):
        if rank in results.keys() and rank in results_position.keys():
            vertical_type = results[rank]['item6']
            result_left = float(results_position[rank]['item3'])
            result_top = float(results_position[rank]['item4'])
            result_width = float(results_position[rank]['item5'])
            result_height = float(results_position[rank]['item6'])
            number_results += 1
            total_height += result_height
            if result_width > total_width:
                total_width = result_width
            if vertical_type != 'organic':
                if vertical_type not in vertical_types:
                    vertical_types.append(vertical_type)
                number_vertical_results += 1
                total_vertical_results_height += result_height
                if rank in images_position.keys():
                    had_image = False
                    for each_image in images_position[rank]:
                        left, top, width, height = each_image
                        left = float(left)
                        top = float(top)
                        width = float(width)
                        height = float(height)
                        right = left + width
                        bottom = top + height
                        is_displayed = True
                        result_right = result_left + result_width
                        result_bottom = result_top + result_height
                        if left < result_left or right > result_right or top < result_top or bottom > result_bottom:
                            is_displayed = False
                        if is_displayed:
                            had_image = True
                            number_images += 1
                            total_images_area += height * width
                    if had_image:
                        number_results_with_images += 1
                        total_results_with_images_height += result_height
    if number_results:
        features['fraction_of_vertical_results_first_screen'] = number_vertical_results / number_results
        features['area_fraction_of_vertical_result_first_screen'] = total_vertical_results_height / total_height
        features['fraction_of_results_with_images_first_screen'] = number_results_with_images / number_results
        features['area_fraction_of_results_with_images_first_screen'] = total_results_with_images_height / total_height
        features['area_fraction_of_images_first_screen'] = total_images_area / (total_height * total_width)
    else:
        features['fraction_of_vertical_results_first_screen'] = 0
        features['area_fraction_of_vertical_result_first_screen'] = 0
        features['fraction_of_results_with_images_first_screen'] = 0
        features['area_fraction_of_results_with_images_first_screen'] = 0
        features['area_fraction_of_images_first_screen'] = 0
    features['number_of_images_first_screen'] = number_images
    features['number_of_vertical_types_first_screen'] = len(vertical_types)
    if 'encyclopedia' in vertical_types:
        features['had_encyclopedia_first_screen'] = 1
    else:
        features['had_encyclopedia_first_screen'] = 0
    if 'gps_map' in vertical_types:
        features['had_gps_map_first_screen'] = 1
    else:
        features['had_gps_map_first_screen'] = 0
    if 'forum' in vertical_types:
        features['had_forum_first_screen'] = 1
    else:
        features['had_forum_first_screen'] = 0
    if 'experience' in vertical_types:
        features['had_experience_first_screen'] = 1
    else:
        features['had_experience_first_screen'] = 0

    number_vertical_results = 0.0
    number_results_with_images = 0.0
    number_images = 0.0
    number_results = 0.0
    total_height = 0.0
    total_width = 0.0
    total_vertical_results_height = 0.0
    total_results_with_images_height = 0.0
    total_images_area = 0.0
    vertical_types = []
    for rank in range(first_screen_end, 11):
        if rank in results.keys() and rank in results_position.keys():
            vertical_type = results[rank]['item6']
            result_left = float(results_position[rank]['item3'])
            result_top = float(results_position[rank]['item4'])
            result_width = float(results_position[rank]['item5'])
            result_height = float(results_position[rank]['item6'])
            number_results += 1
            total_height += result_height
            if result_width > total_width:
                total_width = result_width
            if vertical_type != 'organic':
                if vertical_type not in vertical_types:
                    vertical_types.append(vertical_type)
                number_vertical_results += 1
                total_vertical_results_height += result_height
                if rank in images_position.keys():
                    had_image = False
                    for each_image in images_position[rank]:
                        left, top, width, height = each_image
                        left = float(left)
                        top = float(top)
                        width = float(width)
                        height = float(height)
                        right = left + width
                        bottom = top + height
                        is_displayed = True
                        result_right = result_left + result_width
                        result_bottom = result_top + result_height
                        if left < result_left or right > result_right or top < result_top or bottom > result_bottom:
                            is_displayed = False
                        if is_displayed:
                            had_image = True
                            number_images += 1
                            total_images_area += height * width
                    if had_image:
                        number_results_with_images += 1
                        total_results_with_images_height += result_height
    if number_results:
        features['fraction_of_vertical_results_other_screens'] = number_vertical_results / number_results
        features['area_fraction_of_vertical_result_other_screens'] = total_vertical_results_height / total_height
        features['fraction_of_results_with_images_other_screens'] = number_results_with_images / number_results
        features['area_fraction_of_results_with_images_other_screens'] = total_results_with_images_height / total_height
        features['area_fraction_of_images_other_screens'] = total_images_area / (total_height * total_width)
    else:
        features['fraction_of_vertical_results_other_screens'] = 0
        features['area_fraction_of_vertical_result_other_screens'] = 0
        features['fraction_of_results_with_images_other_screens'] = 0
        features['area_fraction_of_results_with_images_other_screens'] = 0
        features['area_fraction_of_images_other_screens'] = 0
    features['number_of_images_other_screens'] = number_images
    features['number_of_vertical_types_other_screens'] = len(vertical_types)
    if 'encyclopedia' in vertical_types:
        features['had_encyclopedia_other_screens'] = 1
    else:
        features['had_encyclopedia_other_screens'] = 0
    if 'gps_map' in vertical_types:
        features['had_gps_map_other_screens'] = 1
    else:
        features['had_gps_map_other_screens'] = 0
    if 'forum' in vertical_types:
        features['had_forum_other_screens'] = 1
    else:
        features['had_forum_other_screens'] = 0
    if 'experience' in vertical_types:
        features['had_experience_other_screens'] = 1
    else:
        features['had_experience_other_screens'] = 0

    return features


def write_url_features(query, fout_url, baidu_result_features, sogou_result_features, delta_result_features, url_features, screen_url_features):
    fout_url.write(query + '\t')
    for feature in url_features:
        fout_url.write(str(baidu_result_features[feature]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for feature in screen_url_features:
            fout_url.write(str(baidu_result_features[feature+screen]) + '\t')
    for feature in url_features:
        fout_url.write(str(sogou_result_features[feature]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for feature in screen_url_features:
            fout_url.write(str(sogou_result_features[feature+screen]) + '\t')
    for feature in url_features:
        fout_url.write(str(delta_result_features[feature]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for feature in screen_url_features:
            fout_url.write(str(delta_result_features[feature+screen]) + '\t')
    fout_url.write('\n')


def write_text_features(query, fout_text, baidu_result_features, sogou_result_features, delta_result_features, screen_text_features):
    fout_text.write(query + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for elem in ['title_', 'snippet_']:
            for stat in ['max_', 'avg_']:
                for feature in screen_text_features:
                    fout_text.write(str(baidu_result_features[stat + elem + feature + screen]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for elem in ['title_', 'snippet_']:
            for stat in ['max_', 'avg_']:
                for feature in screen_text_features:
                    fout_text.write(str(sogou_result_features[stat + elem + feature + screen]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for elem in ['title_', 'snippet_']:
            for stat in ['max_', 'avg_']:
                for feature in screen_text_features:
                    fout_text.write(str(delta_result_features[stat + elem + feature + screen]) + '\t')
    fout_text.write('\n')


def write_vertical_features(query, fout_vertical, baidu_result_features, sogou_result_features, delta_result_features, vertical_features, screen_vertical_features):
    fout_vertical.write(query + '\t')
    for feature in vertical_features:
        fout_vertical.write(str(baidu_result_features[feature]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for feature in screen_vertical_features:
            fout_vertical.write(str(baidu_result_features[feature + screen]) + '\t')
    for feature in vertical_features:
        fout_vertical.write(str(sogou_result_features[feature]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for feature in screen_vertical_features:
            fout_vertical.write(str(sogou_result_features[feature + screen]) + '\t')
    for feature in vertical_features:
        fout_vertical.write(str(delta_result_features[feature]) + '\t')
    for screen in ['_first_screen', '_other_screens']:
        for feature in screen_vertical_features:
            fout_vertical.write(str(delta_result_features[feature + screen]) + '\t')
    fout_vertical.write('\n')


if __name__ == "__main__":
    results_files = {
        'baidu_results': open('../data/baidu_results_info.txt', 'r'),
        'baidu_results_position': open('../data/baidu_results_position.txt', 'r'),
        'sogou_results': open('../data/sogou_results_info.txt', 'r'),
        'sogou_results_position': open('../data/sogou_results_position.txt', 'r')
    }
    image_files = {
        'baidu_images_position': open('../data/baidu_images_position.txt', 'r'),
        'sogou_images_position': open('../data/sogou_images_position.txt', 'r')
    }
    # results_all_info[filename][query][rank]['item']
    results_all_info = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {})))
    for filename in results_files.keys():
        results_files[filename].readline()
        count = 0
        while True:
            count += 1
            line = results_files[filename].readline().strip()
            if not line:
                break
            if len(line.split('\t')) == 6:
                query, rank, item3, item4, item5, item6 = line.split('\t')
                rank = int(rank)
                results_all_info[filename][query][rank]['item3'] = item3
                results_all_info[filename][query][rank]['item4'] = item4
                results_all_info[filename][query][rank]['item5'] = item5
                results_all_info[filename][query][rank]['item6'] = item6
            else:
                print 'error', line
        results_files[filename].close()
    # images_all_info[filename][query][rank] = [[]]
    images_all_info = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))
    for filename in image_files.keys():
        image_files[filename].readline()
        count = 0
        while True:
            count += 1
            line = image_files[filename].readline().strip()
            if not line:
                break
            if len(line.split('\t')) == 6:
                query, rank, item3, item4, item5, item6 = line.split('\t')
                rank = int(rank)
                images_all_info[filename][query][rank].append([item3, item4, item5, item6])
            else:
                print 'error', line
        image_files[filename].close()

    # features!!!
    url_features = ['reciprocal_of_the_rank_of_the_first_identical_url', 'average_of_reciprocal_of_the_rank_of_the_identical_urls']
    screen_url_features = ['fraction_of_identical_urls', 'had_identical_url']
    screen_text_features = ['char_length', 'word_length', 'matches_fraction_with_query']
    vertical_features = ['reciprocal_of_the_rank_of_the_first_vertical_result', 'position_y_of_the_first_vertical_result', 'height_of_the_first_vertical_result', 'reciprocal_of_the_rank_of_the_first_result_with_image', 'position_y_of_the_first_result_with_image', 'height_of_the_first_result_with_image']
    screen_vertical_features = ['fraction_of_vertical_results', 'area_fraction_of_vertical_result', 'fraction_of_results_with_images', 'area_fraction_of_results_with_images', 'number_of_images', 'area_fraction_of_images', 'number_of_vertical_types', 'had_encyclopedia', 'had_gps_map', 'had_forum', 'had_experience']

    fout_url = open('./url_features.txt', 'w')
    fout_url.write('query\t')
    for group in ['baidu_', 'sogou_', 'delta_']:
        for feature in url_features:
            fout_url.write(group + feature + '\t')
        for screen in ['_first_screen', '_other_screens']:
            for feature in screen_url_features:
                fout_url.write(group + feature + screen + '\t')
    fout_url.write('\n')

    fout_text = open('./text_features.txt', 'w')
    fout_text.write('query\t')
    for group in ['baidu_', 'sogou_', 'delta_']:
        for screen in ['_first_screen', '_other_screens']:
            for elem in ['title_', 'snippet_']:
                for stat in ['max_', 'avg_']:
                    for feature in screen_text_features:
                        fout_text.write(group + stat + elem + feature + screen + '\t')
    fout_text.write('\n')

    fout_vertical = open('./vertical_features.txt', 'w')
    fout_vertical.write('query\t')
    for group in ['baidu_', 'sogou_', 'delta_']:
        for feature in vertical_features:
            fout_vertical.write(group + feature + '\t')
        for screen in ['_first_screen', '_other_screens']:
            for feature in screen_vertical_features:
                fout_vertical.write(group + feature + screen + '\t')
    fout_vertical.write('\n')

    query_lines = open('../data/query.txt', 'r').readlines()
    query_count = 0
    count = 0

    for query in query_lines:
        query = query.strip()
        arguments_dict = {}
        flag = True
        for filename in results_all_info.keys():
            if query not in results_all_info[filename].keys():
                flag = False
        if flag:
            for filename in ["baidu_results_position", "sogou_results_position"]:
                for rank in range(10, 0, -1):
                    if rank in results_all_info[filename][query].keys():
                        if results_all_info[filename][query][rank]['item5'] == '0' or results_all_info[filename][query][rank]['item6'] == '0':
                            last_rank = rank
                            for i in range(rank, 11):
                                if (i+1) in results_all_info[filename][query].keys():
                                    results_all_info[filename][query][i] = results_all_info[filename][query][i+1]
                                else:
                                    last_rank = i
                                    break
                            results_all_info[filename][query].pop(last_rank)

            for filename in results_all_info.keys():
                arguments_dict[filename] = results_all_info[filename][query]
            for filename in images_all_info.keys():
                if query not in images_all_info[filename].keys():
                    arguments_dict[filename] = {}
                else:
                    arguments_dict[filename] = images_all_info[filename][query]

            ret = extract_url_features(arguments_dict['baidu_results'], arguments_dict['sogou_results'])
            if not ret:
                continue
            baidu_identical_urls, sogou_identical_urls = ret  # [{}, {}]

            ret = extract_result_features(query, arguments_dict['baidu_results'], arguments_dict['baidu_results_position'], arguments_dict['baidu_images_position'], baidu_identical_urls)
            if not ret:
                continue
            baidu_result_features = ret  # {}
            ret = extract_result_features(query, arguments_dict['sogou_results'], arguments_dict['sogou_results_position'], arguments_dict['sogou_images_position'], sogou_identical_urls)
            if not ret:
                continue
            sogou_result_features = ret  # {}
            delta_result_features = {}
            for feature in baidu_result_features.keys():
                delta_result_features[feature] = baidu_result_features[feature] - sogou_result_features[feature]

            write_url_features(query, fout_url, baidu_result_features, sogou_result_features, delta_result_features, url_features, screen_url_features)
            write_text_features(query, fout_text, baidu_result_features, sogou_result_features, delta_result_features, screen_text_features)
            write_vertical_features(query, fout_vertical, baidu_result_features, sogou_result_features, delta_result_features, vertical_features, screen_vertical_features)

            query_count += 1
            print query, query_count

    fout_url.close()
    fout_text.close()
    fout_vertical.close()
