import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests

def get_hutime(hd2):
    url = "http://ap.hutime.org/cal/?ival="+hd2+"&ical=103.1&method=conv&ep=b&ocal=101.1&otype=date&oprop=text&oform=gg%20YYYY-MM-dd"

    r = requests.get(url)
    sd = r.text.replace("C.E. ", "").strip()

    return sd

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
            hd2 = year + "-12-30"
    elif l == 2:
        
        year = dd[0]
        month = dd[1]
        if year.isdecimal() and month.isdecimal():
            hd2 = year+"-"+month+"-30"
    elif l == 3:
        year = dd[0]
        month = "12" if dd[1].strip() == "" else dd[1].strip()
        day = "30" if dd[2].strip() == "" else dd[2].strip()
        if year.isdecimal() and month.isdecimal() and day.isdecimal():
            hd2 = year + "-" + month + "-" + day
    return hd2

dirname = "tei"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

uri_prefix = "https://nakamura196.github.io/saji"
uri = "https://nakamura196.github.io/saji/data/data.json"

path = "../docs/data"

g = Graph()

div1_tmp = {}

for i in range(len(files)):
    file = files[i]

    flg_add = True
    stmts = []

    subject = URIRef(uri+"#"+str(i+1))

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    body = root.find(prefix+"body")

    persNames = body.findall(prefix+"persName")

    for i in range(len(persNames)):
        persName = persNames[i]
        # g.add((subject, URIRef("http://example.org/person"), Literal(persName.text)))
        stmts.append((subject, URIRef("http://example.org/person"), Literal(persName.text)))


    placeNames = body.findall(prefix+"placeName")
    for i in range(len(placeNames)):
        placeName = placeNames[i]
        # g.add((subject, URIRef("http://example.org/place"), Literal(placeName.text)))
        stmts.append((subject, URIRef("http://example.org/place"), Literal(placeName.text)))

    dates = body.findall(prefix+"date")
    created = []
    for i in range(len(dates)):
        date = dates[i]
        #g.add((subject, URIRef("http://purl.org/dc/terms/date"), Literal(date.get("when-custom"))))
        #stmts.append((subject, URIRef("http://purl.org/dc/terms/date"), Literal(date.get("when-custom"))))
        
        hd, n_type = get_hd(date)
        if hd != None:
            hd2 = conv_date(hd)
            if hd2 != "unknown":
                sd = get_hutime(hd2)
                # print(sd)
                date.set(n_type, sd)

                if date.get("type") == "created":
                    created.append(sd)

        if date.get("cert"):
            value = "date_cert_"+date.get("cert")
            stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/cert"), Literal(value)))

    if len(created) > 0:
        # g.add((subject, URIRef("http://purl.org/dc/terms/created"),Literal(sorted(created)[0])))
        stmts.append((subject, URIRef("http://purl.org/dc/terms/created"),Literal(sorted(created)[0])))
    else:
        stmts.append((subject, URIRef("http://purl.org/dc/terms/created"),Literal("unknown")))

    divs = body.findall(prefix+"div1")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            value = div.get("type")

            # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"), Literal(div.get("type"))))
            stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type1"), Literal(value)))

            # print(value)

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
            flg = False
            for key in map:

                if key in value:
                    stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type0"), Literal(map[key])))
                    flg = True
                    break

            if not flg:
                print(value)

                if value not in div1_tmp:
                    div1_tmp[value] = 0

                div1_tmp[value] += 1
                

    divs = body.findall(prefix+"div2")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"), Literal(div.get("type"))))
            stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type2"), Literal(div.get("type"))))

    divs = body.findall(prefix+"div3")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            value = div.get("type")

            # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"), Literal(div.get("type"))))
            stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type3"), Literal(value)))

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

                if "カウント" in value:
                    flg_add = False

                # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/note"), Literal(value)))
                stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/note"), Literal(value)))

    title = file.split("/")[-1].split(".")[0]
    # g.add((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))
    stmts.append((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))

    text = ET.tostring(body, encoding='utf-8', method='text')
    text = text.strip()
    if len(text) > 0:
        # g.add((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))
        stmts.append((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))
          
    # tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"\\")[1]
    tei_url = uri_prefix + "/"+dirname+"/" + file.split("/"+dirname+"/")[1]
    # g.add((subject, URIRef("http://purl.org/dc/terms/relation"), URIRef("https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url)))
    stmts.append((subject, URIRef("http://purl.org/dc/terms/relation"), URIRef("https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url)))

    thumbnail = root.find(prefix+"graphic").get("url").replace("/original/", "/medium/")
    # g.add((subject, URIRef("http://xmlns.com/foaf/0.1/thumbnail"), URIRef(thumbnail)))
    stmts.append((subject, URIRef("http://xmlns.com/foaf/0.1/thumbnail"), URIRef(thumbnail)))

    metadata = root.find(prefix+"sourceDesc").find(prefix+"p")
    try:
        metadata_json = json.loads(metadata.text)
    except:
        # print(file)
        a = "a"

    for field in metadata_json:
        value_array = metadata_json[field]
        for value in value_array:
            # g.add((subject, URIRef(field.replace("saji:", "http://diyhistory.org/public/phr2/ns/saji/")), Literal(value)))
            stmts.append((subject, URIRef(field.replace("saji:", "http://diyhistory.org/public/phr2/ns/saji/")), Literal(value)))
    
    if flg_add:
        for stmt in stmts:
            g.add(stmt)

    tree.write(dir.replace("/tei", "/tei3")+"/"+title+".xml", encoding="utf-8")

g.serialize(destination=path+'/data.json', format="json-ld")


print(div1_tmp)