#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'
from collections import defaultdict

fout = open('./output.csv', 'w')
#fout_b_s = open('./output_b_s.csv', 'w')
f_annotation = open('../data/annotation_by_user.txt', 'r')
f_features = {}
f_features['query'] = open('./query_features.txt', 'r')
f_features['url'] = open('./url_features.txt', 'r')
# f_features['text'] = open('./text_features.txt', 'r')
f_features['vertical'] = open('./vertical_features.txt', 'r')

features_name = []
features_dict = defaultdict(lambda: [])
for feature_type in f_features.keys():
    features_index = []
    line = f_features[feature_type].readline().strip()
    line_list = line.split('\t')
    for i in range(1, len(line_list)):
        if 'other_screens' not in line_list[i]:
            features_name.append(line_list[i])
            features_index.append(i)
    while True:
        line = f_features[feature_type].readline().strip()
        if not line:
            break
        line_list = line.split('\t')
        query = line_list[0]
        for i in features_index:
            features_dict[query].append(line_list[i])

annotations_by_user = defaultdict(lambda: {})
users = []
line = f_annotation.readline()
while True:
    line = f_annotation.readline().strip()
    if not line:
        break
    user, query, preference = line.split('\t')
    if user not in users:
        users.append(user)
    annotations_by_user[user][query] = preference

fout.write(','.join(features_name))
fout.write(',preference\n')
count = 0
for query in annotations_by_user[users[3]].keys():
    if query in features_dict.keys():
        if len(features_dict[query]) == 65:
            fout.write(','.join(features_dict[query]))
            fout.write(',')
            if annotations_by_user[users[3]][query] == 'tie':
                fout.write('tie\n')
            else:
                fout.write('different\n')
            count += 1
            print count

'''preference_dict = {}
line = f_annotation.readline().strip()
features_name += line.split('\t')[1:]
while True:
    line = f_annotation.readline().strip()
    if not line:
        break
    query, preference = line.split('\t')
    preference_dict[query] = preference'''

'''fout.write(','.join(features_name))
fout.write('\n')
count = 0
for query in preference_dict.keys():
    if query in features_dict.keys():
        if len(features_dict[query]) == 14:
            fout.write(','.join(features_dict[query]))
            fout.write(',')
            if preference_dict[query] == 'tie':
                fout.write('tie\n')
            else:
                fout.write('different\n')
            count += 1
            print count'''

'''fout_b_s.write(','.join(features_name))
fout_b_s.write('\n')
count = 0
for query in preference_dict.keys():
    if query in features_dict.keys():
        if preference_dict[query] != 'tie':
            if len(features_dict[query]) == 65:
                fout_b_s.write(','.join(features_dict[query]))
                fout_b_s.write(',')
                if preference_dict[query] == 'baidu':
                    fout_b_s.write('baidu\n')
                else:
                    fout_b_s.write('sogou\n')
                count += 1
                print count'''
