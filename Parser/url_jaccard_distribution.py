#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

fout = open('../data/url_jaccard.csv', 'r')
jaccard_num = {0.1: 0, 0.2: 0, 0.3: 0, 0.4: 0, 0.5: 0, 0.6: 0, 0.7: 0, 0.8: 0, 0.9: 0, 1.0: 0}
while True:
    line = fout.readline()
    if not line:
        break
    query, jaccard = line.strip().split(',')
    jaccard = float(jaccard)
    if jaccard <= 0.1:
        jaccard_num[0.1] += 1
    elif jaccard <= 0.2:
        jaccard_num[0.2] += 1
    elif jaccard <= 0.3:
        jaccard_num[0.3] += 1
    elif jaccard <= 0.4:
        jaccard_num[0.4] += 1
    elif jaccard <= 0.5:
        jaccard_num[0.5] += 1
    elif jaccard <= 0.6:
        jaccard_num[0.6] += 1
    elif jaccard <= 0.7:
        jaccard_num[0.7] += 1
    elif jaccard <= 0.8:
        jaccard_num[0.8] += 1
    elif jaccard <= 0.9:
        jaccard_num[0.9] += 1
    else:
        jaccard_num[1.0] += 1
for i in range(1, 11):
    print float(i) / 10, jaccard_num[float(i) / 10]
