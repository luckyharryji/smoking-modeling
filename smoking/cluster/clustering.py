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
        # _x.append(float(data[2]))
        # _y.append(float(data[3]))
            _point.append([float(data[3]),float(data[2])])
            _point_to_id[index_point] = data[0]
            index_point += 1

    return asarray(_point),_point_to_id


import time
import random
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
import json

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

def kmeans_plot(_point,n_clusters_,point_to_id):
    print "points:",_point
    print len(_point)
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_)
    k_means.fit(asarray(_point))
    k_means_labels = k_means.labels_
    print "label: ",k_means_labels
    distinct = dict()
    for index,data in enumerate(k_means_labels):
        print data
        distinct[data] = distinct.get(data,[])
        distinct[data].append(point_to_id[index])

    print len(k_means_labels)
    for index in distinct:
        distinct[index] = len(unique(distinct[index]))
    print distinct
    k_means_cluster_centers = k_means.cluster_centers_
    # print "centers:",k_means_cluster_centers,len(k_means_cluster_centers)
    k_means_labels_unique = unique(k_means_labels)

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
    print point_to_id
    kmeans_plot(points,meaning_shift(points),point_to_id)
