#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation
import matplotlib.pyplot as plt


def get_features_and_ground_truth():
    fin = open('./output.csv', 'r').readlines()[1:]
    features = []
    ground_truth = []
    for line in fin:
        items = line.strip().split(',')
        features.append(items[0:-1])
        preference = items[-1]
        if preference == 'baidu':
            ground_truth.append(0)
        else:
            ground_truth.append(1)

    return features, ground_truth


def human_assist_accuracy(predict_fraction):
    count_right = 0
    predict_number = int(end_ * predict_fraction)
    for i in range(predict_number):
        key = sorted_prob_list[i][0]
        if y_predict[key] == ground_truth[key]:
            count_right += 1
    count_right += end_ - predict_number
    return float(count_right) / float(end_)


if __name__ == "__main__":
    clf = GradientBoostingClassifier()
    features, ground_truth = get_features_and_ground_truth()
    test = ['accuracy', 'recall_macro', 'f1_macro', 'roc_auc']
    for item in test:
        scores = cross_validation.cross_val_score(clf, features, ground_truth, cv=5, scoring=item)
        print(item+" score is "+str(sum(scores)/5))

    gap = len(ground_truth) / 10 + 1
    start_ = 0
    end_ = len(ground_truth)
    y_predict = {}
    y_prob = {}
    number = 0
    count = 0
    for i in range(10):
        start = i * gap
        end = (i + 1)*gap
        X_test, y_test = features[start:min(end, end_)], ground_truth[start:min(end, end_)]
        X_train = features[start_:start] + features[end:end_]
        y_train = ground_truth[start_:start] + ground_truth[end:end_]
        clf.fit(X_train, y_train)
        temp = clf.predict_proba(X_test)
        for item in temp:
            if item[0] <= item[1]:
                y_predict[number] = 1
                y_prob[number] = item[1]
            else:
                y_predict[number] = 0
                y_prob[number] = item[0]
            number += 1

    for i in range(end_):
        if y_predict[i] == ground_truth[i]:
            count += 1
    print float(count) / float(end_)

    sorted_prob_list = sorted(y_prob.iteritems(), key=lambda d:d[1], reverse=True)
    print sorted_prob_list
    human_assist_accuracy_dict = {}
    x = []
    y = []
    for predict_fraction in range(0, 100, 1):
        accuracy = human_assist_accuracy(predict_fraction / 100.0)
        human_assist_accuracy_dict[predict_fraction] = accuracy
        x.append(predict_fraction)
        y.append(accuracy)
    # plot
    plt.scatter(x, y)
    plt.show()
