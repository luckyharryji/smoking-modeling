import matplotlib.pyplot as plt
import random
from numpy import *
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans


def plot_cluster_result(_point,k_means_labels,k_means_cluster_centers,n_clusters_):
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
    ax.set_title('Clustering of Random')
    plt.show()
