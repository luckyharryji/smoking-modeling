### generate different clusters for different time slice: Weekdays, Weekends, and different types: smoke, random(non-smoking)

import sys
sys.path.append("..")
from numpy import *
from collections import Counter
from base.ml_base import k_means as kmeans_plot
from base.ml_base import meaning_shift
from base.load_source_data import import_base_data as data_import
from base.out_data import *

def parse_center(k_means_labels, k_means_cluster_centers,point_to_subject,smoke_type):
    distinct = dict()
    for index,data in enumerate(k_means_labels):
        distinct[data] = distinct.get(data,[])
        distinct[data].append(int(point_to_subject[index]))

    ## get the subject id in each cluster
    cluster_id = list()
    for index in distinct:
        if len(unique(distinct[index]))>10:
            cluster_id.append(list(unique(distinct[index])))

    for index in distinct:
        distinct[index] = len(unique(distinct[index]))
    print distinct

    center_list = list()
    for index in distinct:
        if distinct[index] > 10:
            center_list.append(k_means_cluster_centers[index].tolist())
    to_json('../test/weekend_'+smoke_type+'_center.json',center_list,'weekend_'+smoke_type+'_center',cluster_id)


if __name__=='__main__':
    points, point_to_subject_id =data_import('../data/SmokingData.csv','RANDOM')
    labels, centers = kmeans_plot(points,meaning_shift(points))
    parse_center(labels,centers,point_to_subject_id,'random')
