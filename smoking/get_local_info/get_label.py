from googleplaces import GooglePlaces, types, lang
from numpy import *
import csv
import time
import random
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from sklearn.mixture import GMM
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

def kmeans_plot(_point,n_clusters_,_location):
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_)
    k_means.fit(asarray(_point))
    k_means_labels = k_means.labels_

    gmm = GMM(n_components=n_clusters_, covariance_type='full')
    gmm.fit(asarray(_point))
    _gmm_label = gmm.predict(asarray(_point))

    # iterate the result in the k-means
    for index,data in enumerate(k_means_labels):
        _location[index+1].insert(1,data)
        _location[index+1].insert(2,_gmm_label[index])
        # print data

    with open("output_geo_matrix_kMeans_GMM.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(out_put)

    print "end"
    # k_means_cluster_centers = k_means.cluster_centers_
    # # print "centers:",k_means_cluster_centers,len(k_means_cluster_centers)
    # k_means_labels_unique = unique(k_means_labels)


#


if __name__=='__main__':
    place_type = ['accounting','airport','amusement_park','aquarium','art_gallery','atm','bakery','bank','bar','beauty_salon',
    'bicycle_store','book_store','bowling_alley','bus_station','cafe','campground','car_dealer','car_rental','car_repair','car_wash',
    'casino','cemetery','church','city_hall','clothing_store','convenience_store','courthouse','dentist','department_store',
    'doctor','electrician','electronics_store','embassy','establishment','finance','fire_station','florist','food','funeral_home',
    'furniture_store','gas_station','general_contractor','geocode','grocery_or_supermarket','gym','hair_care','hardware_store','health',
    'hindu_temple','home_goods_store','hospital','insurance_agency','jewelry_store','laundry','lawyer','library','liquor_store',
    'local_government_office','locksmith','lodging','meal_delivery','meal_takeaway','mosque','movie_rental','movie_theater','moving_company',
    'museum','night_club','painter','park','parking','pet_store','pharmacy','physiotherapist','place_of_worship','plumber','police',
    'post_office','real_estate_agency','restaurant','roofing_contractor','rv_park','school','shoe_store','shopping_mall','spa','stadium',
    'storage','store','subway_station','synagogue','taxi_stand','train_station','travel_agency','university','veterinary_care','zoo']

    for k in place_type:
        print k

    with open('../data/SmokingData.csv','rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)
    # _point=list()
    # for index,data in enumerate(raw_data):
    #     if index==0:
    #         continue
    #     _point.append([float(data[3]),float(data[2])])

    out_put = list()

    # change the format of csv file
    out_put.append(['id']+['label_K_Means']+['gmm_label']+raw_data[0]+place_type)
    # print out_put

    with open('near_location_info.json','r') as _f_in:
        geo = json.load(_f_in)

    for id, data in enumerate(raw_data):
        if geo.get(str(id-1)):
            temp = [id-1] + raw_data[id]
            for division in place_type:
                count = 0
                for place in geo[str(id-1)]:
                    if division in place['type']:
                        count += 1
                temp.append(count)
            out_put.append(temp)
            print id


    _point = list()
    for index,row in enumerate(out_put):
        if index == 0:
            continue
        else:
            _point.append(row[6:])
    print _point
    n_cluster = meaning_shift(array(_point))
    kmeans_plot(_point,n_cluster,out_put)
