import json
import pandas as pd

with open('data/items.json') as f:
    df = json.load(f)



map = {}

for item in df:

    title = item["metadata"]["title"]
    
    div1s = item["children"]
    
    types = set()

    for div1 in div1s:
        type_formatted = div1["metadata"]["type_formatted"]
        types.add(type_formatted)

    types = sorted(list(types))
    types_str = "|".join(types).replace("[Missing D] ", "")

    if len(types) == 1:
        formatted_type = types[0]
    else:
        formatted_type = item["metadata"]["type_formatted"] if "[Missing I] " not in item["metadata"]["type_formatted"] else "None"

    # print(title, formatted_type, "|".join(types))
    # rows.append([title, formatted_type, types_str])

    if types_str not in map:
        map[types_str] = {
            "type_formatted": formatted_type,
            "files": []
        }

    map[types_str]["files"].append(title)

rows = []
rows.append(["type", "type_formatted", "files"])

for types_str in map:
    obj = map[types_str]
    rows.append([types_str, obj["type_formatted"], "|".join(obj["files"])])

df = pd.DataFrame(rows)
df.to_csv('data/div1_check.csv', header=False, index=False)