import csv
import sys
import argparse
import json
import requests
import datetime
import yaml
import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json


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


def add_param(type, pid, value, lang):
    obj = {}
    obj["property_id"] = int(pid)
    if type == "literal":
        obj["type"] = type

        obj["@value"] = value
    else:
        obj["type"] = type

        obj["@id"] = value

    if lang != "" and lang != None:
        obj["@language"] = lang

    return obj


if __name__ == "__main__":


    path = "bulletin.xlsx"

    df = pd.read_excel(path, sheet_name=0, header=None, index_col=None)

    r_count = len(df.index)
    c_count = len(df.columns)

    endpoint = "https://diyhistory.org/public/omekas13/api"

    key_identity = "key_identity"
    key_credential = "key_credential"

    url = endpoint + '/items?key_identity=' + key_identity + '&key_credential=' + key_credential

    fields = {}


    for i in range(0, c_count):
        value = df.iloc[0, i]

        if pd.isnull(value):
            continue

        att = value.split("@")

        term = att[0]
        print(term)

        url = endpoint+"/properties?term="+term

        r = requests.get(url)
        data = json.loads(r.content)

        if len(data) == 1:

            obj = {}
            obj["term"] = term
            obj["pid"] = data[0]["o:id"]

            if len(att) == 2:
                obj["lang"] = att[1]

            fields[i] = obj

    print(fields)

    for j in range(1, r_count):

        print(j)

        param = {}

        for i in fields:
            value = df.iloc[j,i]

            if pd.isnull(value):
                continue

            field = fields[i]
            term = field["term"]

            lang = ""
            if "lang" in field:
                lang = field["lang"]

            if term not in param:
                param[term] = []

            param[term].append(add_param("literal", field["pid"], value, lang))

        url = endpoint + '/items?key_identity=' + key_identity + '&key_credential=' + key_credential
        payload = param

        print(param)

        headers = {'content-type': 'application/json; charset=UTF-8'}

        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
        except:
            print("Error.")
