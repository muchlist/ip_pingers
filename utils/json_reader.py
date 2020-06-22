import json


def get_cctv_dict_from_json():
    with open("resource/cctv_banjarmasin.json", "r") as read_file:
        data = json.load(read_file)

    cctv_list_from_json = {}
    for cctv in data:
        name = cctv["cctv_name"] + " " + cctv["location"]
        ip_address = cctv["ip_address"]
        cctv_list_from_json[ip_address] = name

    return cctv_list_from_json

    # with open("Cctv-2020-06-18.json", "w") as write_file:
    # json.dump(data, write_file)
