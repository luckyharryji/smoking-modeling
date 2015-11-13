from googleplaces import GooglePlaces, types, lang
import json
import csv
from settings import API_KEY


def data_import(url):
    with open(url,'rU') as f_in:
        reader = csv.reader(f_in)
        raw_data = list(reader)
    _point=list()
    for index,data in enumerate(raw_data):
        if index==0:
            continue
        _point.append([float(data[3]),float(data[2])])
    return _point

def get_data(axes):
    google_places = GooglePlaces(API_KEY)
    index = 0
    smoke_near = dict()
    miss = list()
    for center in axes:
        s = {'lat':center[1],'lng':center[0]}
        try:
            query_result = google_places.nearby_search(lat_lng=s,radius=800)
            smoke_near[index] = list()
            for place in query_result.places:
                temp = dict()
                temp['name'] = place.name
                # when the name and address are needed, call get_detail first
                # place.get_details()
                temp['type'] = place.types
                smoke_near[index].append(temp)
        except:
            print "connection error"
            miss.append(index)
        index += 1
        print "on going id: ",index
    return smoke_near,miss

def data_write(point,name):
    with open(name,'wr') as f_out:
        f_out.write(json.dumps(point))

if __name__=='__main__':
    axes = data_import('../data/SmokingData.csv')
    location, miss = get_data(axes)
    data_write(location,'near_location_info.json')
    data_write({'points_id':miss},'miss_connect.json')
