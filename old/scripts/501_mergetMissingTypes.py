import json

map = {}

with open('../docs/etc/dict.json') as f:
    df = json.load(f)

    for key in df:
        map[key.lower()] = df[key].lower()

with open('data/missingTypes.json') as f:
    df = json.load(f)

for type in df:
    type = type.lower()
    map[type] = ""

fw = open("../docs/etc/dict.json", 'w')
json.dump(map, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))