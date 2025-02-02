from Items import Items
import glob
from tqdm import tqdm
import copy
import json

def handleFile(file):
    
    
    item = Items(file)

    if item.skip:
        return {}

    item.extractDivs()

    '''
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
    '''

    return {}

dirname = "tei_mod"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

items = []

for i in tqdm(range(len(files))):
    file = files[i]

    if "DSCN2495" not in file:
        continue

    res = handleFile(file)
    if len(res) > 0:
        items.append(res)