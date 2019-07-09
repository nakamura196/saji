import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob

dirname = "tei"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

uri_prefix = "https://nakamura196.github.io/saji"
uri = "https://nakamura196.github.io/saji/data/data.json"

path = "../docs/data"

g = Graph()

for i in range(len(files)):
    file = files[i]

    subject = URIRef(uri+"#"+str(i+1))

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    body = root.find(prefix+"body")

    persNames = body.findall(prefix+"persName")

    for i in range(len(persNames)):
        persName = persNames[i]
        g.add((subject, URIRef("http://example.org/person"), Literal(persName.text)))


    placeNames = body.findall(prefix+"placeName")
    for i in range(len(placeNames)):
        placeName = placeNames[i]
        g.add((subject, URIRef("http://example.org/place"), Literal(placeName.text)))

    dates = body.findall(prefix+"date")
    for i in range(len(dates)):
        date = dates[i]
        g.add((subject, URIRef("http://purl.org/dc/terms/date"),
               Literal(date.get("when-custom"))))

    title = file.split("/")[-1].split(".")[0]
    g.add((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))

    text = ET.tostring(body, encoding='utf-8', method='text')
    text = text.strip()
    if len(text) > 0:
        g.add((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))

    tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"/")[1]
    g.add((subject, URIRef("http://purl.org/dc/terms/relation"),
           URIRef("https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url)))

    thumbnail = root.find(prefix+"graphic").get("url").replace("/original/", "/medium/")
    g.add((subject, URIRef("http://xmlns.com/foaf/0.1/thumbnail"),
           URIRef(thumbnail)))

    metadata = root.find(prefix+"sourceDesc").find(prefix+"p")
    metadata_json = json.loads(metadata.text)

    for field in metadata_json:
        value_array = metadata_json[field]
        for value in value_array:
            g.add((subject, URIRef(field.replace(
                "saji:", "http://diyhistory.org/public/phr2/ns/saji/")), Literal(value)))

g.serialize(destination=path+'/data.json', format="json-ld")


