from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from numpy import *
from base.plot_cluster import plot_cluster_result


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


def k_means(_point,n_clusters_):
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_)
    k_means.fit(asarray(_point))
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    plot_cluster_result(_point,k_means_labels,k_means_cluster_centers,n_clusters_)
    return k_means_labels, k_means_cluster_centers
