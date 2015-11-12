from googleplaces import GooglePlaces, types, lang
import json
import csv



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
out_put.append(['id']+raw_data[0]+place_type)
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


import csv

with open("output_geo_matrix.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(out_put)


#
#     return _point
#
# def get_data(axes):
#     API_KEY = 'AIzaSyAAhvD9lF37p_EDBZKSDHEzNbteQg9pTgQ'
#
#     google_places = GooglePlaces(API_KEY)
#
#     index = 0
#     smoke_near = dict()
#     miss = list()
#     for center in axes:
#         s = {'lat':center[1],'lng':center[0]}
#         try:
#             query_result = google_places.nearby_search(lat_lng=s,radius=300)
#             smoke_near[index] = list()
#             for place in query_result.places:
#                 temp = dict()
#                 temp['name'] = place.name
#                 # place.get_details()
#                 temp['type'] = place.types
#                 smoke_near[index].append(temp)
#         except:
#             print "connection erroe"
#             miss.append(index)
#         index += 1
#         print index
#
#     with open('near_location_info.json','wr') as f_out2:
#         f_out2.write(json.dumps(smoke_near))
#     with open('miss_connect.json','wr') as f_out2:
#         f_out2.write(json.dumps({'points_id':miss}))
#
# if __name__=='__main__':
#     axes = data_import('../data/SmokingData.csv')
#     get_data(axes)
