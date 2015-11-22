import sys
sys.path.append('..')
from settings import place_type
from base.load_source_data import get_json_list
from base.out_data import write_csv


def count_location_number(count_type):
    coordinate = get_json_list('../cluster_feature/'+count_type+'center.json',count_type+'center')
    location_info = get_json_list('../cluster_feature/cluster_map_feature/'+count_type+'near_location_info.json')
    out_put = list()
    out_put.append(['id']+['long']+['altitu']+place_type)
    for index,cor in enumerate(coordinate):
        temp = [index] + cor
        for division in place_type:
            count = 0
            for place in location_info[str(index)]:
                if division in place['type']:
                    count += 1
            temp.append(count)
        out_put.append(temp)
    return out_put

if __name__ == '__main__':
    out_put = count_location_number('weekday_random_')
    write_csv('test_weekday_random.csv',out_put)
