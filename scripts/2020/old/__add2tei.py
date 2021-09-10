import csv
import urllib.request  # ライブラリを取り込む
import os
import json
import glob
import xml.etree.ElementTree as ET

f = open('metadata/data.json', 'r')
metadata = json.load(f)
# ファイルを閉じる
f.close()

metadata_map = {}

for i in range(len(metadata)):
    obj = metadata[i]
    title = obj["dcterms:title"][0]["@value"].split(".")[0]
    metadata_map[title] = {}

    for key in obj:
        if "saji:" in key:
            arr = obj[key]

            metadata_map[title][key] = []

            for a in arr:

                if "@value" in a:
                    value = a["@value"]
                else:
                    value = a["@id"]

                metadata_map[title][key].append(value)

dir = "../docs/tei"
files = glob.glob(dir+"/*.xml")

uri_prefix = "https://nakamura196.github.io/saji"
uri = "https://nakamura196.github.io/saji/data/data.json"

path = "../docs/data"

for i in range(len(files)):
    file = files[i]

    title = file.split("/")[-1].split(".")[0]

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    p = root.find(prefix+"sourceDesc").find(prefix+"p")
    p.text = json.dumps(
        metadata_map[title], ensure_ascii=False, indent=2)

    tree.write(dir.replace("/tei", "/tei2")+"/"+title+".xml", encoding="utf-8")
    # tree.write(dir.replace("/tei", "/tei2")+"/"+title+".xml")


'''

reader = csv.reader(f)
header = next(reader)
for row in reader:
    id = row[7]
    print(id)

    if not os.path.exists(save_name):

        url = "https://diyhistory.org/public/phr2/files/original/"+id+".jpg"

        
        save_name = "original/"+id+".jpg"  # test1.pngという名前で保存される。

        # ダウンロードを実行
        urllib.request.urlretrieve(url, save_name)

f.close()

'''
