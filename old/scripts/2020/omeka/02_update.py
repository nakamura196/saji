import csv
import sys
import argparse
import json
import requests
import datetime
import yaml


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'collection_name',
        action='store',
        type=str,
        help='collection_name')

    parser.add_argument(
        'item_set_id',
        action='store',
        type=str,
        help='item_set_id')

    return parser.parse_args(args)


def get_properties():
    with open("data/properties.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        properties = {}

        for row in reader:
            properties[row[0]] = row[1]

        return properties


def get_ids():
    with open("data/ids.csv", 'r') as f:
        reader = csv.reader(f)
        # header = next(reader)  # ヘッダーを読み飛ばしたい時

        ids = []

        for row in reader:
            ids.append(row[6])

        return ids


def add_param(type, pid, value):
    obj = {}
    obj["property_id"] = int(pid)
    if type == "literal":
        obj["type"] = type

        obj["@value"] = value
    else:
        obj["type"] = type

        obj["@id"] = value

    return obj


if __name__ == "__main__":


    endpoint = "https://diyhistory.org/public/omekas13/api"

    key_identity = "key_identity"
    key_credential = "key_credential"

    oid = 11419

    param = {}

    term = "dcterms:title"

    param[term] = []
    param[term].append(add_param("literal", 1, "タイトルB"))

    term = "dcterms:creator"

    param[term] = []
    param[term].append(add_param("literal", 2, "作成者B"))


    url = endpoint + '/items/'+str(oid)+'?key_identity=' + key_identity + '&key_credential=' + key_credential
    payload = param

    headers = {'content-type': 'application/json; charset=UTF-8'}

    try:
        r = requests.put(url, data=json.dumps(payload), headers=headers)
    except:
        print("Error.")
