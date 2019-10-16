import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import glob
import sys
import argparse
import urllib.parse
import hashlib

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'curation_uri',
        action='store',
        type=str,
        help='curaion uri.')

    parser.add_argument(
        'output_file_path',
        action='store',
        type=str,
        help='output file path.')

    return parser.parse_args(args)

# args = parse_args()

# curation_uri = args.curation_uri
# data_uri = "https://raw.githubusercontent.com/nakamura196/saji/master/docs/data/data.json"

# response = urllib.request.urlopen(data_uri)
# ld_data = json.loads(response.read().decode('utf8'))

with open('../docs/data/data.json') as f:
    ld_data = json.load(f)

# opath = args.output_file_path
opath = "../docs/data/items.json"

size = 10

result = {}
aggregations = {}
aggregations2 = {}

data = []
result["rows"] = data

config = {
    "searchableFields": [],
    "sortings": {
        "Title Asc": {
            "field": '_label',
            "order": 'asc'
        },
        "Title Desc": {
            "field": '_label',
            "order": 'desc'
        }
    },
    "aggregations": aggregations2
}

result["config"] = config

config["searchableFields"].append("_label")
config["searchableFields"].append("_description")
config["searchableFields"].append("_fulltext")

for i in range(len(ld_data)):

    obj = ld_data[i]

    label = obj["http://purl.org/dc/terms/title"][0]["@value"]

    fulltext = label

    obj2 = {
        "_label": label,
        "_related": obj["http://purl.org/dc/terms/relation"][0]["@id"]
    }

    if "http://xmlns.com/foaf/0.1/thumbnail" in obj:
        obj2["_thumbnail"] = obj["http://xmlns.com/foaf/0.1/thumbnail"][0]["@id"]

    for label in obj:
        # if label == "http://purl.org/dc/terms/date" or "/saji/" in label:

        values = obj[label]

        label = label.replace("http://diyhistory.org/public/phr2/ns/saji/", "saji:")
        label = label.replace("http://purl.org/dc/terms/", "dc:")

        for value in values:

            if "@value" in value:

                value = str(value["@value"])

                if "http" not in value:

                    if label not in aggregations:
                        aggregations[label] = {
                            "title": label,
                            "map": {}
                        }

                    if label not in obj2:
                        obj2[label] = []

                    map = aggregations[label]["map"]

                    if value not in map:
                        map[value] = 0

                    map[value] = map[value] + 1

                    obj2[label].append(value)
                    fulltext += " "+value

    obj2["_fulltext"] = fulltext
    data.append(obj2)



for field in aggregations:
    obj = aggregations[field]
    map = obj["map"]
    map = sorted(map.items(), key=lambda kv: kv[1], reverse=True)

    if map[0][1] > 1 and len(map) != 1:
        aggregations2[field] = {
            "title": obj["title"],
            "size": size
        }

f2 = open(opath, 'w')
json.dump(result, f2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))