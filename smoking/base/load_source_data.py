import csv
from numpy import *
import time

def get_csv_dict(URL,get_attribute = None):
    data = list()
    with open(URL) as csv_file:
        data_load = csv.DictReader(csv_file)
        attributes = data_load.fieldnames
        for row in data_load:
            data.append(row)
    if get_attribute:
        return data,attributes
    else:
        return data


def import_base_data(url,smoke_type):
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
        if data[1]==smoke_type:
            date = time.strptime(data[4].split(' ')[0],'%m/%d/%y')
            if date.tm_wday not in [5,6]:
                print date
            else:
                _point.append([float(data[3]),float(data[2])])
                _point_to_id[index_point] = data[0]
                index_point += 1
    return asarray(_point),_point_to_id
