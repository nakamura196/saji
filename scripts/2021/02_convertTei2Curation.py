import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import os
import requests
import json

def getDate(div):
    # <-- 作成年月日の取得
    date = None

    dates  = div.findall(prefix+"date")
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

    return date

def handleDiv(div, file_thumbnail, file_canvas_uri, divStr, mani_data, filename, related):
    

    facs_id = div.get("facs")

    if facs_id == None:
        print("facs: None")
        # continue

        thumbnail = file_thumbnail
        member_id = file_canvas_uri
        label = divStr + "-XXXX"
        media = "No"
        
    else:

        facs_id = facs_id.split(" ")[0].replace("#", "")

        zone = root.find(".//*[@{http://www.w3.org/XML/1998/namespace}id='"+facs_id+"']")

        surface = root.find(".//*[@{http://www.w3.org/XML/1998/namespace}id='"+facs_id+"']/..")

        if surface == None:
            print("**********************", div_str, file)
            return None

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


        member_id = canvas_uri + "#xywh=" + str(x) + ","+str(y)+","+str(w)+","+str(h)
        label = divStr+"-"+id
        media = "Yes"

    metadata = [
        {
            "label": "00_データ単位",
            "value": divStr,
        },
        {
            "label": "テキスト",
            "value": ET.tostring(div, method='text', encoding='unicode'),
        },
        {
            "label": "画像有無",
            "value": media,
        },
        {
            "label": "001_ファイル名",
            "value": filename
        }
    ]

    # divのタイプを取得
    divType = div.get("type")

    anno_type = divType if divType else None
    

    if anno_type:
        metadata.append(
            {
                "label": "02_タイプ",
                "value": anno_type
            })
        metadata.append(
            {
                "label": "01_整形済みタイプ",
                "value": arrangeType(anno_type)
            })

    # ################

    date = getDate(div)

    if date:
        metadata.append({
            "label": "03_作成年月日",
            "value": date,
        })

    # ################

    persNames = body.findall(prefix+"persName") # div1
    for persName in persNames:
        persNameStr = persName.text
        metadata.append({
            "label": "persName",
            "value": persNameStr,
        })

    # ################

    placeNames = body.findall(prefix+"placeName") # div1
    for placeName in placeNames:
        placeNameStr = placeName.text
        metadata.append({
            "label": "placeName",
            "value": placeNameStr,
        })

    # ################

    member = {
        "@id": member_id,
        "@type": "sc:Canvas",
        "label": label,
        "metadata": metadata,
        "thumbnail": thumbnail,
        "related" : related
    }

    return member

def addMembers(members, member):
    if not member:
        return members

    label = member["label"]
    if "XXXX" in label or label not in ids:

        members.append(member)

        ids.append(label)

    return members

def get_mani_data(manifest):

    id = manifest.split("/")[-2]

    path = "../docs/iiif/" + id + "/manifest.json"

    if not os.path.exists(path):
        m = requests.get(manifest).json()

        os.makedirs(os.path.dirname(path), exist_ok=True)

        fw = open(path, 'w')
        json.dump(m, fw, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
        fw.close()

    with open(path) as f:
        data = json.load(f)

    map_ = {}

    canvases = data["sequences"][0]["canvases"]
    for canvas in canvases:
        canvas_id = canvas["@id"]
        service = canvas["thumbnail"]["service"]["@id"]
        map_[canvas_id] = service

    return map_, data["label"].split(".")[0]

def arrangeType(value):
    map = {
        "EMIN": "EMIN",
        "unknown": "unknown",
        "unkown": "unknown",
        "summary_Serbian": "summary_Serbian",
        "summary_Croatian": "summary_Croatian",
        "sumamry_Croatian": "summary_Croatian",
        "summay_Crotatioan": "summary_Croatian",
        "summay_Croatian": "summary_Croatian",
        "summary_Crotatian": "summary_Croatian",
        "summary_Cratian": "summary_Croatian",
        "summary_Craotian": "summary_Croatian",
        "summery_Croatia": "summary_Croatian",
        "hüccet": "hüccet",
        "note": "note",
        "mürāsele": "mürāsele",
        "iʿlām": "iʿlām",
        "tapu": "tapu",
        "buyuruldu": "buyuruldu",
        "kassām": "kassām",
        "Kassām_defteri": "kassām",
        "fetvā": "fetvā",
        "tezkire": "tezkire",
        "fermān": "fermān",
        "ʿilmühaber": "ʿilmühaber",
        "ʿarz-ı_hāl": "ʿarz-ı_hāl",
        "tuğra": "tuğra",
        "şühūdu’l-hāl": "şühūdu’l-hāl",
        "Şühūdu’l-hāl": "şühūdu’l-hāl",
        "zabt_temessük": "temessük",
        "temessük": "temessük",
        "ṣūret": "ṣūret",
        "sūret": "ṣūret",
    }

    for key in map:
        if key in value:
            value = map[key]
            break

    return value

#######################

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
    "label": "オスマン・トルコ語文書群のデータ整理",
    "selections": []
}

count = 1

ld_map = {}

'''
with open('../docs/data/data.json') as f:
    ld = json.load(f)


for obj in ld:
    ld_map[obj["http://purl.org/dc/terms/title"][0]["@value"].replace("tei\\", "")] = obj
'''

properties = {
    '''
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
    '''
}



ids = []

for i in range(len(files)):

    file = files[i]

    filename = file.split("/")[-1].split(".")[0]
    

    

    related = "https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url=https://nakamura196.github.io/saji/tei/"+filename+".xml"

    print(str(i+1)+"/"+str(len(files))+"\t"+file)

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    # <画像の取得>
    surfaceGrp = root.find(prefix+"surfaceGrp")
    manifest = surfaceGrp.get("facs")
    mani_data, label = get_mani_data(manifest)
    # </画像の取得>

    members = []

    body = root.find(prefix+"body")

    #-------------------

    file_thumbnail = ""
    file_canvas_uri = ""


    for canvas_uri in mani_data:
        
        file_canvas_uri = canvas_uri
        file_thumbnail = mani_data[canvas_uri]+"/full/200,/0/default.jpg"

        break

    metadata = [
        {
            "label": "00_データ単位",
            "value": "file",
        },
        {
            "label": "テキスト",
            "value": ET.tostring(body, method='text', encoding='unicode'),
        },
        {
            "label": "画像有無",
            "value": "Yes",
        },
        {
            "label": "001_ファイル名",
            "value": filename
        }
    ]

    date = getDate(body)

    if date:
        metadata.append({
            "label": "03_作成年月日",
            "value": date,
        })

    member = {
        "@id": file_canvas_uri ,
        "@type": "sc:Canvas",
        "label": "file-"+label,
        "metadata": metadata,
        "thumbnail": file_thumbnail,
        "related" : related
    }

    members = addMembers(members, member)

    #-------------------    

    # 第一階層
    div1s = body.findall(prefix+"div1") # div1

    

    for div1 in div1s:

        member = handleDiv(div1, file_thumbnail, file_canvas_uri, "div1", mani_data, filename, related)
        members = addMembers(members, member)

        div_strs = ["div2", "div3"] # *********

        for div_str in div_strs: 
    
            divs = div1.findall(prefix+div_str)
    
            for div in divs:
                
                member = handleDiv(div, file_thumbnail, file_canvas_uri, div_str, mani_data, filename, related)
                members = addMembers(members, member)

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

        count += 1

        curation_data["selections"].append(selection)

    

fw = open("../docs/data/curation.json", 'w')
json.dump(curation_data, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))

