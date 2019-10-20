import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob

import requests
import json

def get_mani_data(manifest):
    headers = {"content-type": "application/json"}
    r = requests.get(manifest, headers=headers)
    data = r.json()

    map_ = {}

    canvases = data["sequences"][0]["canvases"]
    for canvas in canvases:
        canvas_id = canvas["@id"]
        service = canvas["thumbnail"]["service"]["@id"]
        map_[canvas_id] = service

    return map_, data["label"].split(".")[0]


dirname = "tei3"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

curation_uri = "https://nakamura196.github.io/saji/data/curation.json"

curation_data = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@type": "cr:Curation",
    "@id": curation_uri,
    "label": "Automatic curation by TEI",
    "selections": []
}

count = 1

headers = {"content-type": "application/json"}
r = requests.get("https://nakamura196.github.io/saji/data/data.json", headers=headers)
ld = r.json()

ld_map = {}
for obj in ld:
    ld_map[obj["http://purl.org/dc/terms/title"][0]["@value"]] = obj


for i in range(len(files)):

    file = files[i]

    print(str(i+1)+"/"+str(len(files))+"\t"+file)

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    surfaceGrp = root.find(prefix+"surfaceGrp")
    manifest = surfaceGrp.get("facs")

    mani_data, label = get_mani_data(manifest)

    

    surfaces = root.findall(prefix+"surface")

    body = root.find(prefix+"body")

    div1s = body.findall(prefix+"div1")

    members = []

    for div1 in div1s:

        date = None

        dates  = div1.findall(prefix+"date")
        date_arr = []

        for date1 in dates:
            if date1.get("type") == "created":
                value1 = None
                if date1.get("when"):
                    value1 = date1.get("when")
                elif date1.get("from"):
                    value1 = date1.get("from")

                if value1 != None:
                    date_arr.append(value1)

        if len(date_arr) > 0:
            date = date_arr[0]

        div_strs = ["div1", "div2", "div3"]

        for div_str in div_strs: 
    
            divs = div1.findall(prefix+div_str)
    
            for div in divs:

                type = div.get("type")

                facs_id = div.get("facs")
                if facs_id == None:
                    print("facs: None")
                    continue

                facs_id = facs_id[1:]

                zone = root.find(".//*[@{http://www.w3.org/XML/1998/namespace}id='"+facs_id+"']")

                surface = root.find(".//*[@{http://www.w3.org/XML/1998/namespace}id='"+facs_id+"']/..")
                
                if surface == None:
                    print("surface: None")
                    continue

                graphic = surface.find(prefix+"graphic")
                canvas_uri = graphic.get("n")
                
                id = zone.get("{http://www.w3.org/XML/1998/namespace}id")
                ulx = int(zone.get("ulx"))
                uly = int(zone.get("uly"))
                lrx = int(zone.get("lrx"))
                lry = int(zone.get("lry"))

                x = ulx
                y = uly

                w = lrx - x
                h = lry - y

                thumbnail = mani_data[canvas_uri]+"/" + \
                    str(x) + ","+str(y)+","+str(w)+","+str(h)+"/200,/0/default.jpg"

                member = {
                    "@id": canvas_uri + "#xywh=" +
                    str(x) + ","+str(y)+","+str(w)+","+str(h),
                    "@type": "sc:Canvas",
                    "label": id,
                    "metadata": [],
                    "thumbnail": thumbnail

                }

                anno_type = div.get("type") if div.get("type") else None
                text = ET.tostring(div, method='text', encoding='unicode')

                if text:
                    member["text"] = text.strip()

                if anno_type:
                    member["metadata"].append({
                        "label": "type",
                        "value": anno_type
                    })

                if date != None:
                    member["metadata"].append({
                        "label": "date",
                        "value": date
                    })

                members.append(member)

                if label in ld_map:
                    ld = ld_map[label]

                    for key in ld:
                        if "/saji/" in key or "/terms/" in key:
                            values = ld[key]
                            for value in values:
                                if "@value" in value:
                                    member["metadata"].append({
                                        "label": key.replace("http://diyhistory.org/public/phr2/ns/saji/", "saji:").replace("http://purl.org/dc/terms/", "dc:"),
                                        "value": value["@value"]
                                    })

                count += 1

    if len(members) > 0:

        selection = {
            "@id": curation_uri + "/range"+str(count),
            "@type": "sc:Range",
            "label": "Automatic curation by TEI",
            "members": members,
            "within": {
                "@id": manifest,
                "@type": "sc:Manifest",
                "label": root.find(prefix+"title").text
            }
        }

        curation_data["selections"].append(selection)


fw = open("../docs/data/curation_tmp2.json", 'w')
json.dump(curation_data, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))

