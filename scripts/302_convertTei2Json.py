from Item import Item
import glob
from tqdm import tqdm
import copy
import json

dateErrors = {}
missingTypes = set()

def handleFile(file):
    item = Item(file)

    if item.skip:
        return {}

    item.extractMedia()
    item.extractDivs()
    item.extractNotes()
    item.extractSourceDesc()
    item.attachFullText()
    item.attachFormattedType()

    # 日付関係
    item.attachDate()
    item.attachCreated()

    if len(item.dateErrors) > 0:
        dateErrors[item.convert2json()["metadata"]["title"]] = copy.deepcopy(item.dateErrors)

    for type in item.missingTypes:
        missingTypes.add(type)
    
    return copy.deepcopy(item.convert2json())

dirname = "tei_mod"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

items = []

for i in tqdm(range(len(files))):
    file = files[i]
    res = handleFile(file)
    if len(res) > 0:
        items.append(res)
    
fw = open("data/items.json", 'w')
json.dump(items, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
fw.close()

fw = open("data/items.min.json", 'w')
json.dump(items, fw)
fw.close()

fw = open("data/dateErrors.json", 'w')
json.dump(dateErrors, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
fw.close()

fw = open("data/missingTypes.json", 'w')
json.dump(list(missingTypes), fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
fw.close()