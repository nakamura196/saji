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

from bs4 import BeautifulSoup

docs = []
docs.append(["id","title", "date"])

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

path = "../../docs/tei/DSCN0975.xml"

files = glob.glob("../../docs/tei/*.xml")

for path in files:

    with open(path) as doc:
        soup = BeautifulSoup(doc, "xml") # 第2引数でパーサを指定
        # print(soup)

        filename = path.split("/")[-1].split(".")[0]

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


            docs.append([id, title, date_text])



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
                for persName in persNames:
                    name = persName.text
                    role = persName.get("role")

                    '''
                    if role != "" and role != None:

                        name = name + "_" + role
                    '''

                    # print(name)

                    if name not in p_ids:
                        persons.append([name, name, role])
                        p_ids.append(name)

                    

                    # print(role)

                    roles.append([name, id, "CREATED"])

                '''
                persNames = div2.find_all("persname")
                for persName in persNames:
                    name = persName.text
                    role = persName.get("role")

                    # print(name)

                    if name not in p_ids:
                        persons.append([name, name])
                        p_ids.append(name)

                    

                    # print(role)

                    roles.append([name, id, role])
                '''


with open('data/docs.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(docs) # 2次元配列も書き込める

with open('data/docs_r.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(docs_r) # 2次元配列も書き込める

with open('data/persons.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(persons) # 2次元配列も書き込める

with open('data/roles.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(roles) # 2次元配列も書き込める

with open('data/year_r.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(year_r) # 2次元配列も書き込める

with open('data/years.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(years) # 2次元配列も書き込め

with open('data/place_r.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(place_r) # 2次元配列も書き込める

with open('data/places.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(places) # 2次元配列も書き込める

# ----

with open('data/type_r.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(type_r) # 2次元配列も書き込める

with open('data/types.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(types) # 2次元配列も書き込める