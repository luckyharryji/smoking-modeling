import json
import csv

def to_json(URL,data,dic_type,id_dict):
    with open(URL,'wr') as f_out:
        f_out.write(json.dumps({dic_type:data,'subject':id_dict}))
    return

def write_csv(URL,data):
    with open(URL, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print "write csv end"
