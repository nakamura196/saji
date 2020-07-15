import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests
from bs4 import BeautifulSoup

dirname = "tei"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

# uri_prefix = "https://nakamura196.github.io/saji"
# uri = "https://nakamura196.github.io/saji/data/data.json"

# path = "../docs/data"

# g = Graph()

for j in range(len(files)):
    file = files[j]

    # subject = URIRef(uri+"#"+str(i+1))

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    oid = root.find(
        prefix+"surfaceGrp").get("facs").split("/iiif/")[1].split("/")[0]
    print(oid)

    identity = "identity"
    credential = "credential"

    url = "https://diyhistory.org/public/phr4/api/items/"+oid+"?key_identity=" + \
        identity+"&key_credential="+credential

    r = requests.get(url)
    data = r.json()

    body = root.find(prefix+"body")

    manifest = root.find(
        prefix+"surfaceGrp").get("facs")

    data["dcterms:relation"] = [{
        "type": "uri",
        "property_id": 13,
        "@id": "https://diyhistory.org/public/phr4/addon/mirador2/?manifest="+manifest
    }]

    persNames = body.findall(prefix+"persName")

    data["ex:person"] = []

    for i in range(len(persNames)):
        persName = persNames[i]

        data["ex:person"].append({
            "type": "literal",
            "property_id": 370,
            "@value": persName.text
        })

    data["ex:place"] = []

    placeNames = body.findall(prefix+"placeName")
    print(placeNames)
    for i in range(len(persNames)):
        placeName = placeNames[i]

        data["ex:place"].append({
            "type": "literal",
            "property_id": 371,
            "@value": placeName.text
        })

    '''

    placeNames = body.findall(prefix+"placeName")
    for i in range(len(placeNames)):
        placeName = placeNames[i]
        g.add((subject, URIRef("http://example.org/place"), Literal(placeName.text)))

    dates = body.findall(prefix+"date")
    for i in range(len(dates)):
        date = dates[i]
        g.add((subject, URIRef("http://purl.org/dc/terms/date"),
               Literal(date.get("when-custom"))))

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

    '''

    data["ex:fullText"] = []

    fullText = ET.tostring(body)
    fullText = BeautifulSoup(fullText, "lxml").text.strip()

    if fullText != "":
        data["ex:fullText"].append({
            "type": "literal",
            "property_id": 372,
            "@value": fullText
        })

    headers = {'Content-type': 'application/json; charset=UTF-8'}

    # r = requests.put(url, data=json.dumps(payload), headers=headers)
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r)

    '''
    title = file.split("/")[-1].split(".")[0]
    g.add((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))

    text = ET.tostring(body, encoding='utf-8', method='text')
    text = text.strip()
    if len(text) > 0:
        g.add((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))
          
    tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"\\")[1]
    # tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"/")[1]
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

    '''

# g.serialize(destination=path+'/data.json', format="json-ld")


