from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
import requests
import os

"""
Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = '1W2akkXwfDENiC78Cbx1qs3rx39RvIz4ZEGMio0ZMRYs'

with open("data/hutime.json") as f:
    hutime = json.load(f)

def get_hutime(hd2):
    """
    HuTime APIを利用して、ヒジュラ暦の日付を西暦の日付に変換

    Parameters
    --------------
    hd2 : string

    Returns
    -------
    sd : string
        XXXX-XX-XXの形の日付文字列
    """

    url = "http://ap.hutime.org/cal/?ival="+hd2+"&ical=103.1&method=conv&ep=b&ocal=101.1&otype=date&oprop=text&oform=gg%20YYYY-MM-dd"

    r = requests.get(url)
    sd = r.text.replace("C.E. ", "").strip()

    return sd

def get_hd(date):
    """
    ヒジュラ暦の取得

    Parameters
    --------------
    date : xml element

    Returns
    -------
    hd : string
        XXXX-XX-XXの形の日付文字列

    n_type : string
        ノードのタイプ。when, from, toなど。

    """

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
    """
    不足する日付データを修正する。

    Parameters
    --------------
    hd : string
        XXXX-XX-XXの形の日付文字列

    Returns
    -------
    hd2 : string
        XXXX-XX-XXの形の日付文字列

    """
    
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

def add(field, value, map):
    if field not in map:
        map[field] = []
    if value != None:
        map[field].append(value)
    # return map

# 数値→アルファベット
def num2alpha(num):
    if num<=26:
        return chr(64+num)
    elif num%26==0:
        return num2alpha(num//26-1)+chr(90)
    else:
        return num2alpha(num//26)+chr(64+num%26)

dirname = "tei3"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

uri_prefix = "https://nakamura196.github.io/saji"
# uri = "https://nakamura196.github.io/saji/data/data.json"

path = "../docs/data"

# g = Graph()

div1_tmp = {}

items = []

with open('../docs/etc/dict.json') as f:
    dictMap = json.load(f)

print("ファイルサイズ", len(files))

for i in range(len(files)):
    file = files[i]

    if i % 100 == 0:
        print(i+1, len(files), file)

    flg_add = True
    stmts = []
    stmts2 = {}

    # subject = URIRef(uri+"#"+str(i+1))

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    body = root.find(prefix+"body")

    persNames = body.findall(prefix+"persName")

    for i in range(len(persNames)):
        persName = persNames[i]
        # g.add((subject, URIRef("http://example.org/person"), Literal(persName.text)))
        # stmts.append((subject, URIRef("http://example.org/person"), Literal(persName.text)))
        add("tei:persName", persName.text, stmts2)

    placeNames = body.findall(prefix+"placeName")
    for i in range(len(placeNames)):
        placeName = placeNames[i]
        # g.add((subject, URIRef("http://example.org/place"), Literal(placeName.text)))
        # stmts.append((subject, URIRef("http://example.org/place"), Literal(placeName.text)))
        add("tei:placeName", placeName.text, stmts2)

    dates = body.findall(prefix+"date")
    created = []
    for i in range(len(dates)):
        date = dates[i]
        #g.add((subject, URIRef("http://purl.org/dc/terms/date"), Literal(date.get("when-custom"))))
        ## stmts.append((subject, URIRef("http://purl.org/dc/terms/date"), Literal(date.get("when-custom"))))
        add("tei:date", date.get("when-custom"), stmts2)
        
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
            ## stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/cert"), Literal(value)))
            add("tei:cert", value, stmts2)

    if len(created) > 0:
        # g.add((subject, URIRef("http://purl.org/dc/terms/created"),Literal(sorted(created)[0])))
        ## stmts.append((subject, URIRef("http://purl.org/dc/terms/created"),Literal(sorted(created)[0])))
         add("tei:created", sorted(created)[0], stmts2)
        # a = "a"
    else:
        ## stmts.append((subject, URIRef("http://purl.org/dc/terms/created"),Literal("unknown")))
        add("tei:created", "unknown", stmts2)
        # a = "a"

    divs = body.findall(prefix+"div1")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            value = div.get("type")

            # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"), Literal(div.get("type"))))
            ## stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type1"), Literal(value)))
            add("tei:div1", value, stmts2)

            # print(value)

            map = dictMap
            flg = False
            for key in map:

                if key in value:
                    ## stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type0"), Literal(map[key])))
                    add("tei:div1_formatted", map[key], stmts2)
                    flg = True
                    break

            if not flg:
                # print(value)

                if value not in div1_tmp:
                    div1_tmp[value] = 0

                div1_tmp[value] += 1
                

    divs = body.findall(prefix+"div2")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"), Literal(div.get("type"))))
            ## stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type2"), Literal(div.get("type"))))
            add("tei:div2", div.get("type"), stmts2)

            # a = "a"

    divs = body.findall(prefix+"div3")
    for i in range(len(divs)):
        div = divs[i]
        if div.get("type"):

            value = div.get("type")

            # g.add((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type"), Literal(div.get("type"))))
            ## stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/type3"), Literal(value)))
            add("tei:div3", value, stmts2)

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
                ## stmts.append((subject, URIRef("http://diyhistory.org/public/phr2/ns/saji/note"), Literal(value)))
                add("tei:note", value, stmts2)

    title = file.split("/")[-1].split(".")[0]
    # g.add((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))
    ## stmts.append((subject, URIRef("http://purl.org/dc/terms/title"), Literal(title)))
    add("tei:title", title, stmts2)

    text = ET.tostring(body, encoding='utf-8', method='text')
    text = text.strip()
    if len(text) > 0:
        # g.add((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))
        ## stmts.append((subject, URIRef("http://purl.org/dc/terms/description"), Literal(text)))
        
        # これは実施しない
        # add("tei:description", str(text), stmts2)
        # a = "a"
        pass
          
    # tei_url = uri_prefix + "/"+dirname+"/" + file.split("\\"+dirname+"\\")[1]
    tei_url = uri_prefix + "/"+dirname+"/" + file.split(os.sep+dirname+os.sep)[1]
    # g.add((subject, URIRef("http://purl.org/dc/terms/relation"), URIRef("https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url)))
    ## stmts.append((subject, URIRef("http://purl.org/dc/terms/relation"), URIRef("https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url)))
    
    # add("tei:relation", "https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url="+tei_url, stmts2)


    thumbnail = root.find(prefix+"graphic").get("url").replace("/original/", "/medium/")
    # g.add((subject, URIRef("http://xmlns.com/foaf/0.1/thumbnail"), URIRef(thumbnail)))
    ## stmts.append((subject, URIRef("http://xmlns.com/foaf/0.1/thumbnail"), URIRef(thumbnail)))
    
    # add("tei:thumbnail", thumbnail, stmts2)

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
            ## stmts.append((subject, URIRef(field.replace("saji:", "http://diyhistory.org/public/phr2/ns/saji/")), Literal(value)))
            a = "a"
            add(field, value, stmts2)
    
    if flg_add:
        for stmt in stmts:
            # g.add(stmt)
            a = "a"

    # .replace("tei", "tei3")
    # tree.write(dir+"/"+title.replace("tei\\", "")+".xml", encoding="utf-8")

    items.append(stmts2)

    if i > 10000000:
        break

## g.serialize(destination=path+'/data.json', format="json-ld")

data = []
cols = []
for stmt in items:
    for key in stmt:
        if key not in cols:
            cols.append(key)

cols = sorted(cols)
data.append(cols)

for stmt in items:
    row = []
    for i in range(len(cols)):
        value = ""
        col = cols[i]
        if col in stmt:
            value = stmt[col]
        row.append("|".join(value))
    data.append(row)

sheet_name = "item"

range_name = sheet_name+'!A1:'+str(num2alpha(len(cols)))+str(len(data))
value_input_option = 'USER_ENTERED'
values = data
body = {
    'values': values
}
result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    
    valueInputOption=value_input_option, body=body).execute()

print('{0} cells updated.'.format(result.get('updatedCells')))

# -----------------

# div1別
data = []
cols = []
for stmt in items:
    for key in stmt:
        if key not in cols:
            cols.append(key)

cols = sorted(cols)
data.append(cols)

key = "tei:div1_formatted"

for stmt in items:
    if key in stmt:
        div1s = stmt[key]
        for div1 in div1s:
            row = []
            for i in range(len(cols)):
                value = ""
                col = cols[i]
                if col == key:
                    value = [div1]
                elif col in stmt:
                    value = stmt[col]
                row.append("|".join(value))
            data.append(row)

sheet_name = "div1"

range_name = sheet_name+'!A1:'+str(num2alpha(len(cols)))+str(len(data))
value_input_option = 'USER_ENTERED'
values = data
body = {
    'values': values
}
result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    
    valueInputOption=value_input_option, body=body).execute()

print('{0} cells updated.'.format(result.get('updatedCells')))