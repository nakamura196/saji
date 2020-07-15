import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests

date_map = {}

def get_hutime(hd2):
    if hd2 not in date_map:
        
        url = "http://ap.hutime.org/cal/?ival="+hd2+"&ical=103.1&method=conv&ep=b&ocal=101.1&otype=date&oprop=text&oform=gg%20YYYY-MM-dd"

        r = requests.get(url)
        sd = r.text.replace("C.E. ", "").strip()

        date_map[hd2] = sd

        print(len(date_map), hd2)

    return date_map[hd2]

def get_hd(date):

    hd = None
    n_type = None

    if date.get("when-custom"):
        hd = date.get("when-custom")
        n_type = "when"
    elif date.get("from-custom"):
        hd = date.get("from-custom")
        n_type = "from"
    elif date.get("to-custom"):
        hd = date.get("to-custom")
        n_type = "to"

    return hd, n_type


def conv_date(hd):
    
    dd = hd.split("-")

    hd2 = "unknown"
    
    l = len(dd)
    if l == 1:
        year = dd[0]
        if year.isdecimal():
            hd2 = year + "-12-29"
    elif l == 2:
        
        year = dd[0]
        month = dd[1]
        if year.isdecimal() and month.isdecimal():
            hd2 = year+"-"+month+"-29"
    elif l == 3:
        year = dd[0]
        month = "12" if dd[1].strip() == "" else dd[1].strip()
        day = "29" if dd[2].strip() == "" else dd[2].strip()
        if year.isdecimal() and month.isdecimal() and day.isdecimal():
            hd2 = year + "-" + month + "-" + day
    return hd2

dirname = "tei"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

path = "../docs/data"

for l in range(len(files)):
    file = files[l]

    if l % 10 == 0:
        print(l+1, len(files))

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    body = root.find(prefix+"body")

    dates = body.findall(prefix+"date")
    for i in range(len(dates)):
        date = dates[i]
        
        hd, n_type = get_hd(date)
        if hd != None:
            hd2 = conv_date(hd)
            if hd2 != "unknown":
                sd = get_hutime(hd2)
                date.set(n_type, sd)

    title = file.split("/")[-1].split(".")[0]
    tree.write(dir.replace("tei", "tei3")+"/"+title.replace("tei\\", "")+".xml", encoding="utf-8")