#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

import jieba


def extract_query_features(query):
    query_features = []
    char_length = len(query)
    seg_list = jieba.cut(query, cut_all=False)
    word_length = 0
    for item in seg_list:
        word_length += 1
    query_features.append(char_length)
    query_features.append(word_length)
    return query_features

if __name__ == "__main__":
    f_query = open('../data/query.txt', 'r')
    fout = open('./query_features.txt', 'w')
    fout.write('char_length\tword_length\tquery\n')
    while True:
        query = f_query.readline().strip()
        if not query:
            break
        query_features = extract_query_features(query)
        fout.write(str(query_features[0]) + '\t' + str(query_features[1]) + '\t' + query + '\n')
    fout.close()
    f_query.close()
