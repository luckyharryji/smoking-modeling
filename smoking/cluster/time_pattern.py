import csv
from numpy import *
import time
from pylab import *

def data_import(url):
    with open(url,'rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)
    return raw_data


def vis_time_pattern(raw_data):
    subject_id = asarray(raw_data)[1:,0:1]
    result_dict = list()
    for subject in unique(list(subject_id)):
        _week_mon = 0
        _week_noon = 0
        _week_evening = 0
        _week_night = 0

        _end_mon = 0
        _end_noon = 0
        _end_evening = 0
        _end_night = 0

        _r_week_mon = 0
        _r_week_noon = 0
        _r_week_evening = 0
        _r_week_night = 0

        _r_end_mon = 0
        _r_end_noon = 0
        _r_end_evening = 0
        _r_end_night = 0
        print subject
        for index,data in enumerate(raw_data):
            if index==0:
                continue
            if data[0] == subject:
                # print "get"
                if data[1]=='SMOKE':
                    hour = int(data[4].split(' ')[1].split(':')[0])
                    date = time.strptime(data[4].split(' ')[0],'%m/%d/%y')
                    if hour>0 and hour<6:
                        if date.tm_wday in [5,6]:
                            _end_mon += 1
                        else:
                            _week_mon += 1
                    if hour >= 6 and hour < 12:
                        if date.tm_wday in [5,6]:
                            _end_noon += 1
                        else:
                            _week_noon += 1
                    if hour >=12 and hour < 18:
                        if date.tm_wday in [5,6]:
                            _end_evening += 1
                        else:
                            _week_evening += 1
                    if hour >= 18:
                        if date.tm_wday in [5,6]:
                            _end_night += 1
                        else:
                            _week_night += 1
                if data[1]=='RANDOM':
                    hour = int(data[4].split(' ')[1].split(':')[0])
                    date = time.strptime(data[4].split(' ')[0],'%m/%d/%y')
                    if hour>0 and hour<6:
                        if date.tm_wday in [5,6]:
                            _r_end_mon += 1
                        else:
                            _r_week_mon += 1
                    if hour >= 6 and hour < 12:
                        if date.tm_wday in [5,6]:
                            _r_end_noon += 1
                        else:
                            _r_week_noon += 1
                    if hour >=12 and hour < 18:
                        if date.tm_wday in [5,6]:
                            _r_end_evening += 1
                        else:
                            _r_week_evening += 1
                    if hour >= 18:
                        if date.tm_wday in [5,6]:
                            _r_end_night += 1
                        else:
                            _r_week_night += 1
        smoke_week = [_week_mon, _week_noon, _week_evening, _week_night]
        smoke_end = [_end_mon, _end_noon, _end_evening, _end_night]
        random_week = [_r_week_mon, _r_week_noon, _r_week_evening, _r_week_night]
        random_end = [_r_end_mon, _r_end_noon, _r_end_evening, _r_end_night]
        subject_dict = dict()
        subject_dict['id'] = subject
        subject_dict['smoke_weekDay_0_6'] = _week_mon
        subject_dict['smoke_weekDay_6_12'] = _week_noon
        subject_dict['smoke_weekDay_12_18'] = _week_evening
        subject_dict['smoke_weekDay_18_24'] = _week_night
        subject_dict['smoke_weekEnd_0_6'] = _end_mon
        subject_dict['smoke_weekEnd_6_12'] = _end_noon
        subject_dict['smoke_weekEnd_12_18'] = _end_evening
        subject_dict['smoke_weekEnd_18_24'] = _end_night
        subject_dict['random_weekDay_0_6'] = _r_week_mon
        subject_dict['random_weekDay_6_12'] = _r_week_noon
        subject_dict['random_weekDay_12_18'] = _r_week_evening
        subject_dict['random_weekDay_18_24'] = _r_week_night
        subject_dict['random_weekEnd_0_6'] = _r_end_mon
        subject_dict['random_weekEnd_6_12'] = _r_end_noon
        subject_dict['random_weekEnd_12_18'] = _r_end_evening
        subject_dict['random_weekEnd_18_24'] = _r_end_night

        result_dict.append(subject_dict)

        print subject_dict
        fig=plt.figure()
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        fig.suptitle('Subject '+subject+' cout during different time')
        labels = ['0-6', '6-12', '12-18', '18-24']
        plt.plot([1,2,3,4],smoke_week,linewidth = 1,color = 'red',label = 'Smoke Week')
        plt.plot([1,2,3,4],smoke_end,linewidth = 1,color = 'blue',label = 'Smoke Weekends')
        plt.plot([1,2,3,4],random_week,linewidth = 1,color = 'black',label = 'Random Week')
        plt.plot([1,2,3,4],random_end,linewidth = 1,color = 'green',label = 'Random Weekends')
        plt.xticks([1,2,3,4], labels, rotation='vertical')
        plt.legend(loc = 1)
    write_data('../time_pattern/time_pattern.csv',result_dict,['id','smoke_weekDay_0_6','smoke_weekDay_6_12','smoke_weekDay_12_18','smoke_weekDay_18_24','smoke_weekEnd_0_6','smoke_weekEnd_6_12','smoke_weekEnd_12_18','smoke_weekEnd_18_24','random_weekDay_0_6','random_weekDay_6_12','random_weekDay_12_18','random_weekDay_18_24','random_weekEnd_0_6','random_weekEnd_6_12','random_weekEnd_12_18','random_weekEnd_18_24'])


def write_data(URL,data,fields):
    with open(URL, 'w') as csvfile:
        fieldnames = fields
        writer = csv.DictWriter(csvfile,fieldnames = fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__=='__main__':
    points=data_import('../data/SmokingData.csv')
    vis_time_pattern(points)
