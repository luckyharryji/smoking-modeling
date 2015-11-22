import csv
import json

def get_data(URL,filed):
    data = list()
    with open(URL) as csv_file:
        data_load = csv.DictReader(csv_file)
        attributes = data_load.fieldnames
        for row in data_load:
            data.append(row)
    if filed == True:
        return data,attributes
    else:
        return data


def merge_attribute(data1, data2, attributes):
    for row in data1:
        for obj in data2:
            if int(row['SUBJECT']) == int(float(obj['subject'])):
                row['EDUCATE'],row['GENDER'],row['AGE'] = obj['EDUCATE'],obj['GENDER'],obj['AGE']
    attributes.append('EDUCATE')
    attributes.append('GENDER')
    attributes.append('AGE')
    return data1, attributes


def write_data(URL, data,fields):
    with open(URL, 'w') as csvfile:
        fieldnames = fields
        writer = csv.DictWriter(csvfile,fieldnames = fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    user_info = get_data('../base_line/user_output.csv',False)
    location_info , attributes = get_data('../data/all_sample_with_label.csv',True)
    obj_data, fields = merge_attribute(location_info,user_info,attributes)
    write_data('../data/add_baseline.csv',obj_data,fields)
