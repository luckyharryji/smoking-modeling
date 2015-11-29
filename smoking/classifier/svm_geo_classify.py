import json
import csv
from numpy import *
from pylab import *
from sklearn.cross_validation import KFold
from sklearn.svm import SVC

def get_data(URL):
    data = list()
    with open(URL,'rbU') as csvfile:
        reader = csv.reader(csvfile)
        for index,row in enumerate(reader):
            if index == 0:
                continue
            else:
                data.append(row)
    return data

def get_feature(data):
    feature = list()
    for row in data:
        temp = list()
        for num in row[8:]:
            temp.append(int(num))
        feature.append(temp)
    return feature

def get_label(data):
    label = list()
    for row in data:
        if row[4] == 'RANDOM':
            label.append(0)
        else:
            label.append(1)
    return label

if __name__ == '__main__':
    data = get_data('../data/all_sample_with_label.csv')
    # print data
    # print get_label(data)
    feature = array(get_feature(data))
    label = array(get_label(data))
    kf = KFold(len(feature),n_folds = 4,shuffle=True)
    # print len(kf)
    set_index = 0
    for train_index,test_index in kf:
        # print "training set:",train_index,test_index
        print "set : ",set_index
        traing_feature = feature[train_index]
        traing_label = label[train_index]
        test_feature = feature[test_index]
        test_label = label[test_index]
        kernels = ['linear','rbf','sigmoid','poly']
        for kernel in kernels:
            print kernel
            clf = SVC(kernel=kernel)
            clf.fit(traing_feature,traing_label)
            predict = clf.predict(test_feature)
            sum_error = 0
            for index in range(len(predict)):
                if int(predict[index]) != int(test_label[index]):
                    sum_error += 1
            print 'rate: ',float(sum_error)/float(len(predict))
        print
        print
        set_index += 1
