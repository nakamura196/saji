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
        canvas_id =canvas["@id"]
        service = canvas["thumbnail"]["service"]["@id"]
        map_[canvas_id] = service

    return map_


dirname = "tei"
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

for i in range(len(files)):
    file = files[i]

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    surfaceGrp = root.find(prefix+"surfaceGrp")
    manifest = surfaceGrp.get("facs")

    mani_data = get_mani_data(manifest)

    selection = {
        "@id": curation_uri + "/range"+str(count),
        "@type": "sc:Range",
        "label": "Automatic curation by TEI",
        "members": [],
        "within": {
            "@id": manifest,
            "@type": "sc:Manifest",
            "label": root.find(prefix+"title").text
        }
    }

    flg = False

    surfaces = root.findall(prefix+"surface")
    for surface in surfaces:
        graphic = surface.find(prefix+"graphic")
        canvas_uri = graphic.get("n")

        zones = surface.findall(prefix+"zone")

        if len(zones) > 0:
            flg = True

        for zone in zones:
            id = zone.get("{http://www.w3.org/XML/1998/namespace}id")
            ulx = int(zone.get("ulx"))
            uly = int(zone.get("uly"))
            lrx = int(zone.get("lrx"))
            lry = int(zone.get("lry"))

            attr = "#"+id

            #zone_jgh_yhq_h3b

            facs = root.find(".//*[@facs='"+attr+"']")
            anno_type = None
            text = None
            if facs != None:
                anno_type = facs.get("type") if facs.get("type") else None
                text = ET.tostring(facs, method='text', encoding='unicode')

            x = ulx
            y = uly

            w = lrx - x
            h = lry - y

            thumbnail = mani_data[canvas_uri]+"/"+str(x) + ","+str(y)+","+str(w)+","+str(h)+"/200,/0/default.jpg"

            member = {
                "@id": canvas_uri + "#xywh=" +
                str(x) + ","+str(y)+","+str(w)+","+str(h),
                "@type": "sc:Canvas",
                "label": id,
                "metadata": [],
                "thumbnail": thumbnail

            }
            if text:
                member["text"] = text

            if anno_type:
                member["metadata"].append({
                    "label" : "Type",
                    "value" : anno_type
                })

            selection["members"].append(member)

            count += 1

    if flg:
        curation_data["selections"].append(selection)

fw = open("../docs/data/curation.json", 'w')
json.dump(curation_data, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
