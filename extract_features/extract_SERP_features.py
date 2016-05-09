#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'
from collections import defaultdict
import jieba
from selenium import webdriver
import urllib2
from bs4 import BeautifulSoup


def extract_url_features(baidu_results, sogou_results):
    baidu_identical_urls = {}
    sogou_identical_urls = {}

    if len(baidu_results) != len(sogou_results):
        return None
    # 由于url的编码问题,尝试过几种打开url重定向的方法,效果都不是很好...干脆选择比较title的方法
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


def extract_whole_serp_features(results, results_position, images_position):
    vertical_num = 0
    vertical_type_num = 0
    image_num = 0
    vertical_fraction = 0.0
    image_fraction = 0.0

    category_name = []
    for rank in results.keys():
        vertical_type = results[rank]['item6']
        if vertical_type != 'organic':
            vertical_num += 1
            if vertical_type not in category_name:
                category_name.append(vertical_type)
    vertical_type_num = len(category_name)

    total_height = 0.0
    total_width = 0.0
    vertical_total_height = 0.0
    for rank in results_position.keys():
        try:
            vertical_type = results[rank]['item6']
            height = float(results_position[rank]['item6'])
            total_height += height
            width = float(results_position[rank]['item5'])
            if width > total_width:
                total_width = width
            if vertical_type != 'organic':
                vertical_total_height += height
        except:
            return None
    try:
        vertical_fraction = vertical_total_height / total_height
    except:
        return None

    images_total_area = 0.0
    for rank in images_position.keys():
        for each_image in images_position[rank]:
            try:
                left, top, width, height = each_image
                left = float(left)
                top = float(top)
                width = float(width)
                height = float(height)
                right = left + width
                bottom = top + height
                is_displayed = True
                result_left = float(results_position[rank]['item3'])
                result_top = float(results_position[rank]['item4'])
                result_width = float(results_position[rank]['item5'])
                result_height = float(results_position[rank]['item6'])
                result_right = result_left + result_width
                result_bottom = result_top + result_height
                if left < result_left or right > result_right or top < result_top or bottom > result_bottom:
                    is_displayed = False
                if is_displayed:
                    image_num += 1
                    images_total_area += width * height
            except:
                return None
    try:
        image_fraction = images_total_area / (total_width * total_height)
    except:
        return None

    return [vertical_num, vertical_type_num, vertical_fraction, image_num, image_fraction]


def extract_result_features(query, results, results_position, images_position, identical_urls):
    results_features_dict = {}
    last_organic_rank = 0
    last_organic_bottom = 0.0
    last_vertical_rank = 0
    last_vertical_bottom = 0.0

    for rank in range(1, 11):
        try:
            features = {}
            title = results[rank]['item3']
            snippet = results[rank]['item4']
            vertical_type = results[rank]['item6']
            result_left = float(results_position[rank]['item3'])
            result_top = float(results_position[rank]['item4'])
            result_width = float(results_position[rank]['item5'])
            result_height = float(results_position[rank]['item6'])

            features['vertical_type'] = vertical_type
            features['position_y'] = result_top
            features['height'] = result_height
            if vertical_type == 'organic':
                features['is_vertical'] = 0
                last_organic_rank += 1
                features['rank_by_type'] = last_organic_rank
                if last_organic_bottom:
                    features['distance_by_type'] = result_top - last_organic_bottom
                else:
                    features['distance_by_type'] = 0
                last_organic_bottom = result_top + result_height
            else:
                features['is_vertical'] = 1
                last_vertical_rank += 1
                features['rank_by_type'] = last_vertical_rank
                if last_vertical_bottom:
                    features['distance_by_type'] = result_top - last_vertical_bottom
                else:
                    features['distance_by_type'] = 0
                last_vertical_bottom = result_top + result_height
            if identical_urls[rank]:
                features['is_identical_url'] = 1
            else:
                features['is_identical_url'] = 0

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
            features['title_char_length'] = title_char_length
            features['title_word_length'] = title_word_length
            features['snippet_char_length'] = snippet_char_length
            features['snippet_word_length'] = snippet_word_length
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
            features['title_matches'] = title_matches
            features['snippet_matches'] = snippet_matches

            features['images_number'] = 0
            features['images_area_fraction'] = 0.0
            features['had_image'] = 0
            if rank in images_position.keys():
                images_total_number = 0
                images_total_area = 0.0
                for each_image in images_position[rank]:
                    try:
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
                            images_total_number += 1
                            images_total_area += width * height
                    except:
                        continue
                features['images_number'] = images_total_number
                if images_total_number:
                    features['had_image'] = 1
                try:
                    features['images_area_fraction'] = images_total_area / (result_height * result_width)
                except:
                    pass

            results_features_dict[rank] = features
        except:
            features['vertical_type'] = ''
            features['position_y'] = 0
            features['height'] = 0
            features['is_vertical'] = 0
            features['rank_by_type'] = 0
            features['distance_by_type'] = 0
            features['is_identical_url'] = 0
            features['title_char_length'] = 0
            features['title_word_length'] = 0
            features['snippet_char_length'] = 0
            features['snippet_word_length'] = 0
            features['title_matches'] = 0
            features['snippet_matches'] = 0
            features['images_number'] = 0
            features['images_area_fraction'] = 0
            features['had_image'] = 0
            results_features_dict[rank] = features

    return results_features_dict


def write_features_to_files(fout, query, baidu_whole_serp_features, sogou_whole_serp_features, baidu_result_features, sogou_result_features):
    fout.write(query + '\t' + str(baidu_whole_serp_features[1]) + '\t' + str(baidu_whole_serp_features[0]) + '\t' + str(baidu_whole_serp_features[2]) + '\t' + str(baidu_whole_serp_features[3]) + '\t' + str(baidu_whole_serp_features[4]) + '\t')
    for rank in range(1, 11):
        fout.write(str(baidu_result_features[rank]['rank_by_type']) + '\t' + str(baidu_result_features[rank]['position_y']) + '\t' + str(baidu_result_features[rank]['height']) + '\t' + str(baidu_result_features[rank]['distance_by_type']) + '\t' + str(baidu_result_features[rank]['title_char_length']) + '\t' + str(baidu_result_features[rank]['title_word_length']) + '\t' + str(baidu_result_features[rank]['title_matches']) + '\t' + str(baidu_result_features[rank]['snippet_char_length']) + '\t' + str(baidu_result_features[rank]['snippet_word_length']) + '\t' + str(baidu_result_features[rank]['snippet_matches']) + '\t' + str(baidu_result_features[rank]['vertical_type']) + '\t' + str(baidu_result_features[rank]['images_number']) + '\t' + str(baidu_result_features[rank]['images_area_fraction']) + '\t' + str(baidu_result_features[rank]['is_vertical']) + '\t' + str(baidu_result_features[rank]['is_identical_url']) + '\t' + str(baidu_result_features[rank]['had_image']) + '\t')

    fout.write(str(sogou_whole_serp_features[1]) + '\t' + str(sogou_whole_serp_features[0]) + '\t' + str(sogou_whole_serp_features[2]) + '\t' + str(sogou_whole_serp_features[3]) + '\t' + str(sogou_whole_serp_features[4]) + '\t')
    for rank in range(1, 11):
        fout.write(str(sogou_result_features[rank]['rank_by_type']) + '\t' + str(sogou_result_features[rank]['position_y']) + '\t' + str(sogou_result_features[rank]['height']) + '\t' + str(sogou_result_features[rank]['distance_by_type']) + '\t' + str(sogou_result_features[rank]['title_char_length']) + '\t' + str(sogou_result_features[rank]['title_word_length']) + '\t' + str(sogou_result_features[rank]['title_matches']) + '\t' + str(sogou_result_features[rank]['snippet_char_length']) + '\t' + str(sogou_result_features[rank]['snippet_word_length']) + '\t' + str(sogou_result_features[rank]['snippet_matches']) + '\t' + str(sogou_result_features[rank]['vertical_type']) + '\t' + str(sogou_result_features[rank]['images_number']) + '\t' + str(sogou_result_features[rank]['images_area_fraction']) + '\t' + str(sogou_result_features[rank]['is_vertical']) + '\t' + str(sogou_result_features[rank]['is_identical_url']) + '\t' + str(sogou_result_features[rank]['had_image']) + '\t')

    fout.write(str(baidu_whole_serp_features[1] - sogou_whole_serp_features[1]) + '\t' + str(baidu_whole_serp_features[0] - sogou_whole_serp_features[0]) + '\t' + str(baidu_whole_serp_features[2] - sogou_whole_serp_features[2]) + '\t' + str(baidu_whole_serp_features[3] - sogou_whole_serp_features[3]) + '\t' + str(baidu_whole_serp_features[4] - sogou_whole_serp_features[4]) + '\t')
    for rank in range(1, 11):
        fout.write(str(baidu_result_features[rank]['position_y'] - sogou_result_features[rank]['position_y']) + '\t' + str(baidu_result_features[rank]['height'] - sogou_result_features[rank]['height']) + '\t' + str(baidu_result_features[rank]['title_char_length'] - sogou_result_features[rank]['title_char_length']) + '\t' + str(baidu_result_features[rank]['title_word_length'] - sogou_result_features[rank]['title_word_length']) + '\t' + str(baidu_result_features[rank]['title_matches'] - sogou_result_features[rank]['title_matches']) + '\t' + str(baidu_result_features[rank]['snippet_char_length'] - sogou_result_features[rank]['snippet_char_length']) + '\t' + str(baidu_result_features[rank]['snippet_word_length'] - sogou_result_features[rank]['snippet_word_length']) + '\t' + str(baidu_result_features[rank]['snippet_matches'] - sogou_result_features[rank]['snippet_matches']) + '\t' + str(baidu_result_features[rank]['images_number'] - sogou_result_features[rank]['images_number']) + '\t' + str(baidu_result_features[rank]['images_area_fraction'] - sogou_result_features[rank]['images_area_fraction']) + '\t' + str(baidu_result_features[rank]['is_vertical'] - sogou_result_features[rank]['is_vertical']) + '\t' + str(baidu_result_features[rank]['is_identical_url'] - sogou_result_features[rank]['is_identical_url']) + '\t' + str(baidu_result_features[rank]['had_image'] - sogou_result_features[rank]['had_image']) + '\t')

    fout.write('\n')


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
    # results_all_info[filename][query][rank][ ]
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
    # images_all_info[filename][query][rank]
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

    query_lines = open('../data/query.txt', 'r').readlines()
    query_count = 0

    fout = open('./SERP_features.txt', 'w')
    fout.write('query\tbaidu_vertical_types_number\tbaidu_vertical_results_number\tbaidu_vertical_results_area_fraction\tbaidu_total_images_number\tbaidu_total_images_area_fraction\t')
    for i in range(1, 11):
        fout.write('baidu_rank_by_type_' + str(i) + '\tbaidu_position_y_' + str(i) + '\tbaidu_height_' + str(i) + '\tbaidu_distance_by_type_' + str(i) + '\tbaidu_title_char_length_' + str(i) + '\tbaidu_title_word_length_' + str(i) + '\tbaidu_title_matches_' + str(i) + '\tbaidu_snippet_char_length_' + str(i) + '\tbaidu_snippet_word_length_' + str(i) + '\tbaidu_snippet_matches_' + str(i) + '\tbaidu_vertical_type_' + str(i) + '\tbaidu_images_number_' + str(i) + '\tbaidu_images_area_fraction_' + str(i) + '\tbaidu_is_vertical_' + str(i) + '\tbaidu_is_identical_url_' + str(i) + '\tbaidu_had_image_' + str(i) + '\t')

    fout.write('sogou_vertical_types_number\tsogou_vertical_results_number\tsogou_vertical_results_area_fraction\tsogou_total_images_number\tsogou_total_images_area_fraction\t')
    for i in range(1, 11):
        fout.write('sogou_rank_by_type_' + str(i) + '\tsogou_position_y_' + str(i) + '\tsogou_height_' + str(i) + '\tsogou_distance_by_type_' + str(i) + '\tsogou_title_char_length_' + str(i) + '\tsogou_title_word_length_' + str(i) + '\tsogou_title_matches_' + str(i) + '\tsogou_snippet_char_length_' + str(i) + '\tsogou_snippet_word_length_' + str(i) + '\tsogou_snippet_matches_' + str(i) + '\tsogou_vertical_type_' + str(i) + '\tsogou_images_number_' + str(i) + '\tsogou_images_area_fraction_' + str(i) + '\tsogou_is_vertical_' + str(i) + '\tsogou_is_identical_url_' + str(i) + '\tsogou_had_image_' + str(i) + '\t')

    fout.write('delta_vertical_types_number\tdelta_vertical_results_number\tdelta_vertical_results_area_fraction\tdelta_total_images_number\tdelta_total_images_area_fraction\t')
    for i in range(1, 11):
        fout.write('delta_position_y_' + str(i) + '\tdelta_height_' + str(i) + '\tdelta_title_char_length_' + str(i) + '\tdelta_title_word_length_' + str(i) + '\tdelta_title_matches_' + str(i) + '\tdelta_snippet_char_length_' + str(i) + '\tdelta_snippet_word_length_' + str(i) + '\tdelta_snippet_matches_' + str(i) + '\tdelta_images_number_' + str(i) + '\tdelta_images_area_fraction_' + str(i) + '\tdelta_is_vertical_' + str(i) + '\tdelta_is_identical_url_' + str(i) + '\tdelta_had_image_' + str(i) + '\t')
    fout.write('\n')

    for query in query_lines:
        query = query.strip()
        arguments_dict = {}
        flag = True
        for filename in results_all_info.keys():
            if query not in results_all_info[filename].keys():
                flag = False
        if flag:
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

            ret = extract_whole_serp_features(arguments_dict['baidu_results'], arguments_dict['baidu_results_position'], arguments_dict['baidu_images_position'])
            if not ret:
                continue
            baidu_whole_serp_features = ret  # []
            ret = extract_whole_serp_features(arguments_dict['sogou_results'], arguments_dict['sogou_results_position'], arguments_dict['sogou_images_position'])
            if not ret:
                continue
            sogou_whole_serp_features = ret  # []

            ret = extract_result_features(query, arguments_dict['baidu_results'], arguments_dict['baidu_results_position'], arguments_dict['baidu_images_position'], baidu_identical_urls)
            if not ret:
                continue
            baidu_result_features = ret  # { {} }
            ret = extract_result_features(query, arguments_dict['sogou_results'], arguments_dict['sogou_results_position'], arguments_dict['sogou_images_position'], sogou_identical_urls)
            if not ret:
                continue
            sogou_result_features = ret  # { {} }
            '''
            fout_bwsf = open('./baidu_whole_serp_features.txt', 'w')
            fout_swsf = open('./sogou_whole_serp_features.txt', 'w')
            fout_wsf_delta = open('./delta_whole_serp_features.txt', 'w')
            fout_brf = open('./baidu_rank_features.txt', 'w')
            fout_srf = open('./sogou_rank_features.txt', 'w')
            fout_rf_delta = open('./delta_rank_features.txt', 'w')
            fout_bpf = open('./baidu_position_features.txt', 'w')
            fout_spf = open('./sogou_position_features.txt', 'w')
            fout_pf_delta = open('./delta_rank_features.txt', 'w')
            fout_btf = open('./baidu_text_features.txt', 'w')
            fout_stf = open('./sogou_text_features.txt', 'w')
            fout_tf_delta = open('./delta_text_features', 'w')
            fout_bvf = open('./baidu_vertical_features', 'w')
            fout_svf = open('./sogou_vertical_features', 'w')
            fout_vf_delta = open('./delta_vertical_features', 'w')
            fout_bbf = open('./baidu_binary_features', 'w')
            fout_sbf = open('./sogou_binary_features', 'w')
            fout_bf_delta = open('./delta_binary_features', 'w')
            '''

            write_features_to_files(fout, query, baidu_whole_serp_features, sogou_whole_serp_features, baidu_result_features, sogou_result_features)

            query_count += 1
            print query, query_count

    fout.close()
