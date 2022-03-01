from Item import Item
import glob
from tqdm import tqdm
import copy
import json

def handleFile(file):
    
    
    item = Item(file)

    if item.skip:
        return {}

    item.extractDivs()
    '''
    item.extractMedia()
    item.extractCreated()
    
    item.extractNotes()
    item.extractSourceDesc()
    item.attachFullText()
    '''
    item.extractNotes()
    item.attachDate()
    item.attachCreated()
    
    return copy.deepcopy(item.convert2json())

dirname = "tei3"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

items = []

for i in tqdm(range(len(files))):
    file = files[i]
    res = handleFile(file)
    if len(res) > 0:
        items.append(res)

filename = "400_test_date"
    
fw = open("data/{}.json".format(filename), 'w')
json.dump(items, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
fw.close()