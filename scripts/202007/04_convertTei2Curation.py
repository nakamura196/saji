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
files = sorted(files)

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

'''
headers = {"content-type": "application/json"}
r = requests.get("https://nakamura196.github.io/saji/data/data.json", headers=headers)
ld = r.json()
'''

with open('../docs/data/data.json') as f:
    ld = json.load(f)

ld_map = {}
for obj in ld:
    ld_map[obj["http://purl.org/dc/terms/title"][0]["@value"].replace("tei\\", "")] = obj

properties = {
    "http://diyhistory.org/public/phr2/ns/saji/aspectRatioType" : {
        "label" : "ファイル：aspectRatio",
        "term" : "saji:aspectRatioType",
    },
    "http://diyhistory.org/public/phr2/ns/saji/cert" : {
        "label" : "ファイル：作成年月日の確かさ",
        "term" : "saji:cert",
    },
    "http://diyhistory.org/public/phr2/ns/saji/fond" : {
        "label" : "ファイル：フォルダ",
        "term" : "saji:fond",
    },
    "http://diyhistory.org/public/phr2/ns/saji/note" : {
        "label" : "ファイル：備考",
        "term" : "saji:note",
    },
    "http://diyhistory.org/public/phr2/ns/saji/type0" : {
        "label" : "ファイル：DIV1の整形済みタイプ",
        "term" : "saji:type0",
        "description" : "EMIN XXXX => EMIN など",
    },
    "http://diyhistory.org/public/phr2/ns/saji/type1" : {
        "label" : "ファイル：DIV1タイプ",
        "term" : "saji:type1"
    },
    "http://diyhistory.org/public/phr2/ns/saji/type2" : {
        "label" : "ファイル：DIV2タイプ",
        "term" : "saji:type2"
    },
    "http://diyhistory.org/public/phr2/ns/saji/type3" : {
        "label" : "ファイル：DIV3タイプ",
        "term" : "saji:type3"
    },
    "http://purl.org/dc/terms/created" : {
        "label" : "ファイル：作成年月日",
        "term" : "dcterms:created",
        "description" : "複数ある場合には最も若い値",
        "type" : "date"
    },
    "http://purl.org/dc/terms/description" : {
        "label" : "ファイル：テキスト",
        "term" : "dcterms:description"
    },
    "http://purl.org/dc/terms/title" : {
        "label" : "ファイル：名前",
        "term" : "dcterms:title"
    },
    "http://diyhistory.org/public/phr2/ns/saji/memo" : {
        "label" : "Omeka：メモ",
        "term" : "saji:memo"
    },
    "http://diyhistory.org/public/phr2/ns/saji/type" : {
        "label" : "Omeka：タイプ",
        "term" : "saji:type",
    },
    "http://diyhistory.org/public/phr2/ns/saji/transcription" : {
        "label" : "Omeka：翻刻文",
        "term" : "saji:transcription"
    },
    "http://diyhistory.org/public/phr2/ns/saji/relationWithAnotherItems" : {
        "label" : "Omeka：他アイテムとの関係",
        "term" : "saji:relationWithAnotherItems"
    },
    "http://diyhistory.org/public/phr2/ns/saji/date_M" : {
        "label" : "Omeka：date_M",
        "term" : "saji:date_M"
    },
    "http://diyhistory.org/public/phr2/ns/saji/calligraphy" : {
        "label" : "Omeka：calligraphy",
        "term" : "saji:calligraphy"
    },
    "http://diyhistory.org/public/phr2/ns/saji/date_H" : {
        "label" : "Omeka：date_H",
        "term" : "saji:date_H"
    },
    "http://diyhistory.org/public/phr2/ns/saji/foldingMethod" : {
        "label" : "Omeka：foldingMethod",
        "term" : "saji:foldingMethod"
    },
    "http://diyhistory.org/public/phr2/ns/saji/huve" : {
        "label" : "Omeka：huve",
        "term" : "saji:huve"
    },
    "http://diyhistory.org/public/phr2/ns/saji/item" : {
        "label" : "Omeka：item",
        "term" : "saji:item"
    },
    "http://diyhistory.org/public/phr2/ns/saji/lang" : {
        "label" : "Omeka：lang",
        "term" : "saji:lang"
    },
    "http://diyhistory.org/public/phr2/ns/saji/lineage" : {
        "label" : "Omeka：lineage",
        "term" : "saji:lineage"
    },
    "http://diyhistory.org/public/phr2/ns/saji/number" : {
        "label" : "Omeka：number",
        "term" : "saji:number"
    },
    "http://diyhistory.org/public/phr2/ns/saji/openingPhrase" : {
        "label" : "Omeka：openingPhrase",
        "term" : "saji:openingPhrase"
    },
    "http://diyhistory.org/public/phr2/ns/saji/placeFull" : {
        "label" : "Omeka：placeFull",
        "term" : "saji:placeFull"
    },
    "http://diyhistory.org/public/phr2/ns/saji/stamp_c" : {
        "label" : "Omeka：stamp_c",
        "term" : "saji:stamp_c"
    },
    "http://diyhistory.org/public/phr2/ns/saji/stamp_o" : {
        "label" : "Omeka：stamp_o",
        "term" : "saji:stamp_o"
    },
    "http://diyhistory.org/public/phr2/ns/saji/from" : {
        "label" : "Omeka：from",
        "term" : "saji:from"
    },
    "http://diyhistory.org/public/phr2/ns/saji/witness" : {
        "label" : "Omeka：witness",
        "term" : "saji:witness"
    }
}

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

    # 第一階層
    div1s = body.findall(prefix+"div1")

    members = []

    for div1 in div1s:

        # <-- 作成年月日の取得
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

        # --> 作成年月日の取得

        div_strs = ["div1", "div2", "div3"]

        for div_str in div_strs: 
    
            divs = div1.findall(prefix+div_str)
    
            for div in divs:
                
                # divのタイプを取得
                divType = div.get("type")

                facs_id = div.get("facs")
                if facs_id == None:
                    print("facs: None")
                    continue

                facs_id = facs_id.replace("#", "")

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

                anno_type = divType if divType else None
                text = ET.tostring(div, method='text', encoding='unicode')

                if text:
                    # member["text"] = text.strip()
                    member["metadata"].append({
                        "label": "DIV：各テキスト",
                        "value": text,
                        "term" : "fulltext"
                    })

                if anno_type:
                    member["metadata"].append({
                        "label": "DIV：各DIVタイプ",
                        "value": anno_type,
                        "term" : "type",
                        "description" : "div1-3 type='XXX'",
                    })

                if date != None:
                    member["metadata"].append({
                        "label": "DIV：DIV1の作成年月日",
                        "value": date,
                        "term": "date",
                        "description" : "type='created'",
                        "type" : "date"
                    })

                members.append(member)

                if label in ld_map:
                    ld = ld_map[label]

                    for key in ld:

                        if key == "http://purl.org/dc/terms/relation":
                            member["related"] = ld[key][0]["@id"]


                        if "/saji/" in key or "/terms/" in key:
                            values = ld[key]
                            for value in values:
                                if "@value" in value:
                                    if key in properties:
                                        prop = properties[key]

                                        tmp = {
                                            "label": prop["label"],
                                            "value": value["@value"],
                                            "term" : prop["term"]
                                        }

                                        if "type" in prop:
                                            tmp["type"] = prop["type"]

                                        member["metadata"].append(tmp)
                                    else:
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


fw = open("../docs/data/curation.json", 'w')
json.dump(curation_data, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))

