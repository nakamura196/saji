import shutil
import requests
import os
import json
import glob
import yaml
import sys
import urllib
import ssl
import csv
import time
import hashlib

docs_dir = "../../docs"

path = docs_dir + "/data/curation.json"

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    idMap = {}

    for selection in selections:
        members = selection["members"]

        for member in members:

            uri = member["@id"]
            id = hashlib.md5(uri.encode('utf-8')).hexdigest()

            idMap[id] = uri

    for selection in selections:
        members = selection["members"]

        for member in members:

            thumbnail = member["thumbnail"]

            uri = member["@id"]
            id = hashlib.md5(uri.encode('utf-8')).hexdigest()

            path = "data/json/similar_images/"+id+".json"

            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)

                images = []
                max = 20
                if len(data) < max:
                    max = len(data)
                for i in range(0, max):
                    images.append(idMap[data[i]])
                member["images"] = images

with open(docs_dir + "/data/curation.json", 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))