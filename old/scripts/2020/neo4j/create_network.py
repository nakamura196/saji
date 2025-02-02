from py2neo.data import Node, Relationship
from py2neo import Graph, Node, Relationship

import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
import glob
import csv
import requests
import json
import os
from bs4 import BeautifulSoup

g = Graph("bolt://localhost:7687")

docs = []
docs.append(["id","title", "date", "url"])

# ----------

places = []
places.append(["id","title"])
place_ids = []

place_r = []
place_r.append(["docId","placeId"])

# ----------

types = []
types.append(["id","title"])
type_ids = []

type_r = []
type_r.append(["docId","typeId"])

# ----------

years = []
years.append(["id","title"])
year_ids = []

year_r = []
year_r.append(["docId","yearId"])

# ----------

docs_r = []
docs_r.append(["prev","next", "p"])

doc_ids = []

persons = []
persons.append(["id","name"])

p_ids = []

roles = []
roles.append(["personId","docId", "role"])

# -----------------

dirname = "tei3"

files = glob.glob("../../docs/"+dirname+"/*.xml")


uri_prefix = "https://nakamura196.github.io/saji"

for path in files:

    with open(path) as doc:
        soup = BeautifulSoup(doc, "xml") # 第2引数でパーサを指定
        # print(soup)

        filename = path.split("/")[-1].split(".")[0]

        
        tei_url = uri_prefix + "/"+dirname+"/" + path.split(os.sep+dirname+os.sep)[1]
        url = "https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url


        div1s = soup.find_all("div1")

        prev = None

        for div1 in div1s:
            type = div1.get("type").split(" ")[0]
            # print(type)

            facs = div1.get("facs")
            if facs == None:
                print(facs)
                continue

            id = div1.get("facs").split("#")[1]

            if id in doc_ids:
                continue

            if prev != None:
                docs_r.append([prev, id, "NEXT"])
            
            prev = id

            doc_ids.append(id)

            title = filename+div1.get("facs")
            
            # ---

            date_text = ""

            dates = div1.find_all("date")
            for date in dates:
                # print(date.text)

                date_text = date.text
                if date.get("custom"):
                    date_text = date.get("custom")
                elif date.get("from-custom"):
                    date_text = date.get("from-custom")
                
                # print(date_text)

                if len(date_text.split("-")) == 3:

                    year = date_text.split("-")[0]

                    if year.isdigit():

                        if year not in year_ids:
                            years.append([year, year])
                            year_ids.append(year)
                        
                        year_r.append([id, year])


            
            docs.append([id, title, date_text, url])



            # ---

            placeNames = div1.find_all("placeName")
            for placeName in placeNames:
                # print(date.text)

                place = placeName.text

                if place not in place_ids:
                    places.append([place, place])
                    place_ids.append(place)
                
                place_r.append([id, place])

            # ---

            if type != None:

                if type not in type_ids:
                    types.append([type, type])
                    type_ids.append(type)
                
                type_r.append([id, type])

            # ---

            div2s = div1.find_all("div2")
            for div2 in div2s:
                persNames = div2.find_all("persName")
                # print(div2.get("type"))
                for persName in persNames:
                    name = persName.text
                    role = persName.get("role")

                    if name not in p_ids:
                        persons.append([name, name, role])
                        p_ids.append(name)

                    roles.append([name, id, div2.get("type")])

docs_map = {}
persons_map = {}

for i in range(1, len(docs)):
    row = docs[i]
    d = Node("Document", id=row[0], title=row[1], date=row[2], url=row[3])
    # docs.append(["id","title", "date", "url"])
    docs_map[row[0]] = d
    g.merge(d, "Document", "id")

for i in range(1, len(docs_r)):
    row = docs_r[i]
    p = Relationship.type("NEXT")
    g.merge(p(docs_map[row[0]], docs_map[row[1]]), "Document", "id")
    # docs_r.append(["prev","next", "p"])

# persons.append(["id","name"])
for i in range(1, len(persons)):
    row = persons[i]
    n = Node("Person", id=row[0], name=row[1])
    # docs.append(["id","title", "date", "url"])
    persons_map[row[0]] = n
    g.merge(n, "Person", "id")

for i in range(1, len(roles)):
    row = roles[i]
    p = Relationship.type(row[2])
    if row[0] not in persons_map:
        print("row[0] not in persons_map")
        continue
    n1 = persons_map[row[0]]
    n2 = docs_map[row[1]]
    g.merge(p(n1, n2), "Person", "id")

years_map = {}

for i in range(1, len(years)):
    row = years[i]
    n = Node("Year", id=row[0], title=row[1])
    # docs.append(["id","title", "date", "url"])
    years_map[row[0]] = n
    g.merge(n, "Year", "id")

for i in range(1, len(year_r)):
    row = year_r[i]
    p = Relationship.type("CREATED")
    n1 = docs_map[row[0]]
    n2 = years_map[row[1]]
    g.merge(p(n1, n2), "Document", "id")

places_map = {}

for i in range(1, len(places)):
    row = places[i]
    n = Node("Place", id=row[0], title=row[1])
    # docs.append(["id","title", "date", "url"])
    places_map[row[0]] = n
    g.merge(n, "Place", "id")

for i in range(1, len(place_r)):
    row = place_r[i]
    p = Relationship.type("PLACE")
    n1 = docs_map[row[0]]
    n2 = places_map[row[1]]
    g.merge(p(n1, n2), "Document", "id")

types_map = {}

for i in range(1, len(types)):
    row = types[i]
    n = Node("Type", id=row[0], title=row[1])
    types_map[row[0]] = n
    g.merge(n, "Type", "id")

for i in range(1, len(type_r)):
    row = type_r[i]
    p = Relationship.type("TYPE")
    n1 = docs_map[row[0]]
    n2 = types_map[row[1]]
    g.merge(p(n1, n2), "Document", "id")