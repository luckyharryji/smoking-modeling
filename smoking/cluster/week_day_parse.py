import csv
from numpy import *
import time
from pylab import *
import time
import random
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
import json

def data_import(url):
    with open(url,'rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)
    subject_id = asarray(raw_data)[1:,0:1]


    result_dict = list()

    for subject in unique(list(subject_id)):
        smoke = dict()
        random = dict()
        for i in range(7):
            smoke[i] = 0
            random[i] = 0



        # print subject
        for index,data in enumerate(raw_data):
            if index==0:
                continue
            if data[0] == subject:
                # print "get"
                if data[1]=='SMOKE':
                    hour = int(data[4].split(' ')[1].split(':')[0])
                    date = time.strptime(data[4].split(' ')[0],'%m/%d/%y')
                    smoke[date.tm_wday] += 1

                if data[1]=='RANDOM':
                    hour = int(data[4].split(' ')[1].split(':')[0])
                    date = time.strptime(data[4].split(' ')[0],'%m/%d/%y')
                    random[date.tm_wday] += 1
        _smoke_show = list()
        _random_show = list()
        for i in range(7):
            _smoke_show.append(smoke[i])
            _random_show.append(random[i])

        fig=plt.figure()
        plt.xlabel('Day of week')
        plt.ylabel('Frequency')
        # yscale(log)
        fig.suptitle('Subject '+subject+' cout during different day of week')
        labels = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        plt.plot([1,2,3,4,5,6,7],_smoke_show,linewidth = 1,color = 'red',label = 'Smoke')
        plt.plot([1,2,3,4,5,6,7],_random_show,linewidth = 1,color = 'blue',label = 'Random')
        plt.xticks([1,2,3,4,5,6,7], labels, rotation='vertical')
        plt.legend(loc = 1)
        savefig('../week_day_pattern/'+subject+'_week_day.png')
    # write_data('../time_pattern/time_pattern.csv',result_dict,['id','smoke_weekDay_0_6','smoke_weekDay_6_12','smoke_weekDay_12_18','smoke_weekDay_18_24','smoke_weekEnd_0_6','smoke_weekEnd_6_12','smoke_weekEnd_12_18','smoke_weekEnd_18_24','random_weekDay_0_6','random_weekDay_6_12','random_weekDay_12_18','random_weekDay_18_24','random_weekEnd_0_6','random_weekEnd_6_12','random_weekEnd_12_18','random_weekEnd_18_24'])


def write_data(URL,data,fields):
    with open(URL, 'w') as csvfile:
        fieldnames = fields
        writer = csv.DictWriter(csvfile,fieldnames = fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__=='__main__':
    points=data_import('../data/SmokingData.csv')
    # print points
    # kmeans_plot(points,meaning_shift(points))
