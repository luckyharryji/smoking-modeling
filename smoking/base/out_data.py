import json

def to_json(URL,data,dic_type,id_dict):
    with open(URL,'wr') as f_out:
        f_out.write(json.dumps({dic_type:data,'subject':id_dict}))
    return
