import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests

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
    created = []
    for i in range(len(dates)):
        date = dates[i]
        g.add((subject, URIRef("http://purl.org/dc/terms/date"),
               Literal(date.get("when-custom"))))
        if date.get("type") == "created":
            
            if date.get("when-custom"):
                hd = date.get("when-custom")
            elif date.get("from-custom"):
                hd = date.get("from-custom")
            if hd != None and len(hd) == 10:
                
                url = "http://ap.hutime.org/cal/?ival="+hd+"&ical=103.1&method=conv&ep=b&ocal=101.1&otype=date&oprop=text&oform=gg%20YYYY-MM-dd"

                r = requests.get(url)
                sd = r.text.replace("C.E. ", "").strip()
                
                # g.add((subject, URIRef("http://purl.org/dc/terms/created"),Literal(sd)))
                created.append(sd)

    if len(created) > 0:
        g.add((subject, URIRef("http://purl.org/dc/terms/created"),Literal(sorted(created)[0])))

    divs = body.findall(prefix+"div")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"),
                Literal(div.get("type"))))

    notesStmt = root.find(prefix+"notesStmt")
    if notesStmt != None:
        notes = notesStmt.findall(prefix+"note")
        for i in range(len(notes)):
            note = notes[i]

            if note.text:

                type = ""
                if note.get("type"):
                    type = note.get("type")+": "

                value = type + note.text 

                g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/note"),
                    Literal(value)))

    title = file.split("/")[-1].split(".")[0]
    g.add((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))

    text = ET.tostring(body, encoding='utf-8', method='text')
    text = text.strip()
    if len(text) > 0:
        g.add((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))
          
    # tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"\\")[1]
    tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"/")[1]
    g.add((subject, URIRef("http://purl.org/dc/terms/relation"),
           URIRef("https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url)))

    thumbnail = root.find(prefix+"graphic").get("url").replace("/original/", "/medium/")
    g.add((subject, URIRef("http://xmlns.com/foaf/0.1/thumbnail"),
           URIRef(thumbnail)))

    metadata = root.find(prefix+"sourceDesc").find(prefix+"p")
    try:
        metadata_json = json.loads(metadata.text)
    except:
        print(file)

    for field in metadata_json:
        value_array = metadata_json[field]
        for value in value_array:
            g.add((subject, URIRef(field.replace(
                "saji:", "http://diyhistory.org/public/phr2/ns/saji/")), Literal(value)))

g.serialize(destination=path+'/data.json', format="json-ld")


