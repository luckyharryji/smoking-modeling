import csv
from numpy import *
import time

def data_import(url):
    with open(url,'rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)

    _x=[]
    _y=[]
    _point_1=list()
    _point_2=list()
    _point_3=list()
    _point_4=list()

    for index,data in enumerate(raw_data):
        if index==0:
            continue
        if data[1]=='SMOKE':
            date = time.strptime(data[4].split(' ')[0],'%m/%d/%y')
            # print hour
            if date.tm_wday in [5,6]:
                print date
                _point_1.append([float(data[3]),float(data[2])])
    # return 1
    return asarray(_point_1)


import time
import random
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
import json

def meaning_shift(_point):
    bandwidth = estimate_bandwidth(_point, quantile=0.2)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(_point)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = unique(labels)
    n_clusters = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters)
    return n_clusters

def kmeans_plot(_point,n_clusters_):
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_)
    k_means.fit(asarray(_point))
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = unique(k_means_labels)

    # with open('random_center.json','wr') as f_out:
    #     f_out.write(json.dumps({'center':k_means_cluster_centers.tolist()}))
    # plot the result of k-means
    fig = plt.figure()
    r = lambda: random.randint(0,255)
    colors = ['#%02X%02X%02X' % (r(),r(),r()) for countnums in range(22)]

    X = asarray(_point)
    ax = fig.add_subplot(111)

    for k, col in zip(range(n_clusters_), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
                markerfacecolor=col, marker='.',markersize=8)
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k')

    ax.set_title('Clustering of smoking in weekends')
    plt.show()

if __name__=='__main__':
    points=data_import('../data/SmokingData.csv')
    kmeans_plot(points,meaning_shift(points))
