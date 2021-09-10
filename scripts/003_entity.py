import json
import glob
import os
import json
from bs4 import BeautifulSoup

#######################

dirname = "tei3"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")
files = sorted(files)

oDir = "../../u-renja/static/data"

configs = [
    {
        "id": "person",
        "tag": "persName"
    },
    {
        "id": "place",
        "tag": "placeName"
    }
]

map = {}

for config in configs:
    map[config["id"]] = {}

for i in range(len(files)):

    file = files[i]

    filename = file.split("/")[-1].split(".")[0]
    
    if i % 300 == 0:
        print(str(i+1)+"/"+str(len(files))+"\t"+file)

    soup = BeautifulSoup(open(file,'r'), "xml")

    ######

    body = soup.find("body")

    if not body:
        continue

    for config in configs:

        conf_id = config["id"]
        conf_tag = config["tag"]

        map4index = map[conf_id]

        tags = body.find_all(conf_tag)
        for tag in tags:
            
            name = tag.text

            id = filename + "_" + name.replace(" ", "_").replace("\t", "_t_").replace("\n", "_n_")

            if id not in map4index:
                item = {
                    "objectID": id,
                    "label": name,
                    "file": [],
                    "fulltext": name
                }

                map4index[id] = item

            item = map4index[id]
            if filename not in item["file"]:
                item["file"].append(filename)

for config in configs:
    conf_id = config["id"]
    map4index = map[conf_id]
    index = []
    for id in map4index:

        item = map4index[id]

        item_path = oDir + "/item/" + id + ".json"

        os.makedirs(os.path.dirname(item_path), exist_ok=True)

        fw = open(item_path, 'w')
        json.dump(item, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

        index.append(
            item
        )

    fw = open(oDir + "/" +conf_id+ ".json", 'w')
    json.dump(index, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

