from googleplaces import GooglePlaces, types, lang
import json
import csv


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
    with open('miss_connect.json') as f_in:
        miss_id = json.load(f_in)
    miss_id = miss_id['points_id']
    with open('near_location_info.json') as f_in2:
        # f_out2.write(json.dumps(smoke_near))
        smoke_near = json.load(f_in2)
    for identifer in miss_id:
        center = axes[identifer]
        s = {'lat':center[1],'lng':center[0]}
        try:
            query_result = google_places.nearby_search(lat_lng=s,radius=300)
            smoke_near[identifer] = list()
            for place in query_result.places:
                temp = dict()
                temp['name'] = place.name
                # place.get_details()
                temp['type'] = place.types
                smoke_near[identifer].append(temp)
        except:
            print "connection error"
            miss.append(identifer)
    with open('near_location_re_get_miss.json','wr') as f_out:
        f_out.write(json.dumps(smoke_near))
    with open('miss_connect_re_getting.json','wr') as f_out2:
        f_out2.write(json.dumps({'points_id':miss}))




if __name__=='__main__':
    axes = data_import('../data/SmokingData.csv')
    get_data(axes)
