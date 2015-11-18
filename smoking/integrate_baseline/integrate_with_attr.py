import csv
from numpy import *

def data_import(url):
    with open(url,'rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)
    _x=[]
    _y=[]
    _point=list()

    _point_to_id = dict()
    index_point = 0
    for index,data in enumerate(raw_data):
        if index==0:
            continue
        if data[1]=='SMOKE':
            _point.append([float(data[3]),float(data[2])])
            _point_to_id[index_point] = data[0]
            index_point += 1

    return asarray(_point),_point_to_id


import time
import random
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
import json
from collections import Counter

def meaning_shift(_point):
    bandwidth = estimate_bandwidth(_point, quantile=0.5)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(_point)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = unique(labels)
    n_clusters = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters)
    return n_clusters


def get_data(URL,filed):
    data = list()
    with open(URL) as csv_file:
        data_load = csv.DictReader(csv_file)
        attributes = data_load.fieldnames
        for row in data_load:
            data.append(row)
    if filed == True:
        return data,attributes
    else:
        return data

def merge_attribute(data1, data2, attributes):
    for row in data1:
        for obj in data2:
            if int(row['SUBJECT']) == int(float(obj['subject'])):
                row['EDUCATE'],row['GENDER'],row['AGE'],row['JOB'],row['LOCTIME'] = obj['EDUCATE'],obj['GENDER'],obj['AGE'],obj['JOB'],obj['LOCTIME']
    attributes.append('EDUCATE')
    attributes.append('GENDER')
    attributes.append('AGE')
    attributes.append('JOB')
    attributes.append('LOCTIME')
    return data1, attributes

def kmeans_plot(_point,n_clusters_,point_to_id):
    # print "points:",_point
    # print len(_point)
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_)
    k_means.fit(asarray(_point))
    k_means_labels = k_means.labels_
    # print "label: ",k_means_labels
    distinct = dict()
    for index,data in enumerate(k_means_labels):
        distinct[data] = distinct.get(data,[])
        distinct[data].append(int(point_to_id[index]))

    # print len(k_means_labels)
    for index in distinct:
        print list(unique(distinct[index]))
        # distinct[index] = len(unique(distinct[index]))
    print distinct
    k_means_cluster_centers = k_means.cluster_centers_
    print "centers:",k_means_cluster_centers,len(k_means_cluster_centers)
    k_means_labels_unique = unique(k_means_labels)

    user_info = get_data('../temp_data/base_line_attr.csv',False)
    result = []
    for index in distinct:
        temp = dict()
        temp['cluster_id'] = int(index)
        temp['cluster_center'] = list(k_means_cluster_centers[index])
        educatte = []
        gender = []
        age = []
        job = []
        loctime = []
        print list(unique(distinct[index]))
        for subject in list(unique(distinct[index])):
            # print int(row['SUBJECT'])
            for row in user_info:
                # print row['SUBJECT'],subject,type(row['SUBJECT']),type(subject)
                if int(row['SUBJECT']) == subject:
                    # print "get"
                    educatte.append(row['EDUCATE'])
                    gender.append(row['GENDER'])
                    age.append(row['AGE'])
                    job.append(row['JOB'])
                    loctime.append(row['LOCTIME'])
                    break
        # print educatte
        temp['education'] = count_ratio(educatte)
        temp['gender'] = count_ratio(gender)
        temp['age'] = count_ratio(age)
        temp['job'] = count_ratio(job)
        temp['locatime'] = count_ratio(loctime)
        result.append(temp)
    print result
    with open('../temp_data/cluster_count.json','wr') as f_out:
        f_out.write(json.dumps(result))

def count_ratio(data):
    obj = dict()
    num = Counter(data)
    for i in num:
        obj[str(i)] = float(num[i])/len(data)
    return obj




    # with open('random_center.json','wr') as f_out:
    #     f_out.write(json.dumps({'center':k_means_cluster_centers.tolist()}))
    # plot the result of k-means
    # fig = plt.figure()
    # r = lambda: random.randint(0,255)
    # colors = ['#%02X%02X%02X' % (r(),r(),r()) for countnums in range(22)]
    #
    # X = asarray(_point)
    # ax = fig.add_subplot(111)
    #
    # for k, col in zip(range(n_clusters_), colors):
    #     my_members = k_means_labels == k
    #     cluster_center = k_means_cluster_centers[k]
    #     ax.plot(X[my_members, 0], X[my_members, 1], 'w',
    #             markerfacecolor=col, marker='.',markersize=8)
    #     ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #             markeredgecolor='k')
    #
    # ax.set_title('Clustering of Random')
    # plt.show()

if __name__=='__main__':
    points, point_to_id =data_import('../data/SmokingData.csv')
    # print point_to_id
    kmeans_plot(points,meaning_shift(points),point_to_id)
