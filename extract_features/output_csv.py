#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

fout = open('./output_weak.csv', 'w')
f_annotation = open('../data/annotation_weak.txt', 'r')
f_query_features = open('./query_features.txt', 'r')
f_serp_features = open('./SERP_features.txt', 'r')
features_name = []

query_features_dict = {}
line = f_query_features.readline().strip()
features_name += line.split('\t')[1:]
while True:
    line = f_query_features.readline().strip()
    if not line:
        break
    query, char_length, word_length = line.split('\t')
    query_features_dict[query] = [char_length, word_length]

serp_features_dict = {}
line = f_serp_features.readline().strip()
features_name += line.split('\t')[1:]
while True:
    line = f_serp_features.readline().strip()
    if not line:
        break
    line_list = line.split('\t')
    query = line_list[0]
    serp_features_dict[query] = line_list[1:]

preference_dict = {}
line = f_annotation.readline().strip()
features_name += line.split('\t')[1:]
while True:
    line = f_annotation.readline().strip()
    if not line:
        break
    query, preference = line.split('\t')
    preference_dict[query] = preference

fout.write(','.join(features_name))
fout.write('\n')
count = 0
for query in preference_dict.keys():
    if query in query_features_dict and query in serp_features_dict:
        fout.write(','.join(query_features_dict[query] + serp_features_dict[query]))
        fout.write(',')
        if preference_dict[query] == 'tie':
            fout.write('tie\n')
        else:
            fout.write('different\n')
        count += 1
        print count
