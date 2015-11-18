from googleplaces import GooglePlaces, types, lang
from numpy import *
import csv
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from sklearn.mixture import GMM
import json
from settings import place_type


def load_data(URL,type_user):
    with open(URL,'rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)
    _point=list()
    for index,data in enumerate(raw_data):
        if index==0:
            _point.append(data)
            continue
        if data[1]==type_user:
            _point.append([index-1]+data)
    return _point


def load_json(URL):
    with open(URL,'r') as _f_in:
        geo = json.load(_f_in)
    return geo

def write_csv(URL,data):
    with open(URL, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print "write csv end"


def meaning_shift(_point,quantile):
    bandwidth = estimate_bandwidth(_point, quantile=quantile)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(_point)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    labels_unique = unique(labels)
    n_clusters = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters)
    return n_clusters

def kmeans_plot(_point,n_clusters_,_location):
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_)
    k_means.fit(asarray(_point))
    k_means_labels = k_means.labels_

    gmm = GMM(n_components=n_clusters_, covariance_type='full')
    gmm.fit(asarray(_point))
    _gmm_label = gmm.predict(asarray(_point))

    for index,data in enumerate(k_means_labels):
        _location[index+1].insert(1,data)
        _location[index+1].insert(2,_gmm_label[index])
    return _location

if __name__=='__main__':
    raw_data = load_data('../data/SmokingData.csv','RANDOM')
    out_put = list()
    out_put.append(['id']+['label_K_Means']+['gmm_label']+raw_data[0]+place_type)

    geo = load_json('../temp_data/all_location.json')

    for id, data in enumerate(raw_data):
        # print data[0]
        if geo.get(str(data[0])):
            # print "get"
            temp = data
            for division in place_type:
                count = 0
                for place in geo[str(data[0])]:
                    if division in place['type']:
                        count += 1
                temp.append(count)
            out_put.append(temp)

    _point = list()
    for index,row in enumerate(out_put):
        if index == 0:
            continue
        else:
            _point.append(row[6:])
    # print _point

    n_cluster = meaning_shift(array(_point),0.5)
    out_put = kmeans_plot(_point,n_cluster,out_put)
    write_csv("../temp_data/random_with_label.csv",out_put)
