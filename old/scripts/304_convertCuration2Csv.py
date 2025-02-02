import json
import pandas as pd

with open('../docs/data/curation.json') as f:
    df = json.load(f)

    selections = df["selections"]

    keys = set()

    items = []
    div1s = []

    for selection in selections:
        members = selection["members"]

        for member in members:
            metadata = member["metadata"]

            item = {}

            element = None

            for m in metadata:
                label = m["label"]
                value = m["value"]

                keys.add(label)

                if type(value) is list:
                    try:
                        value = "|".join(value)
                    except Exception as e:
                        print(member["label"], e)
                        value = ""

                item[label] = value

                if label == "element":
                    element = value

            if element == "item":
                items.append(item)

            elif element == "div1":
                div1s.append(item)

print("len(items)", len(items))
print("len(div1s)", len(div1s))

rows = []
rows4div1 = []

row = []
rows.append(row)
rows4div1.append(row)

keys = sorted(keys)

for key in keys:
    row.append(key)


for item in items:
    row = []
    rows.append(row)
    for key in keys:
        value = ""
        if key in item:
            # row.append(item[key])
            value = item[key]
        row.append(value)

for item in div1s:
    row = []
    rows4div1.append(row)
    for key in keys:
        value = ""
        if key in item:
            # row.append(item[key])
            value = item[key]
        row.append(value)

df = pd.DataFrame(rows)
df.to_csv('data/item.csv', header=False, index=False)

df = pd.DataFrame(rows4div1)
df.to_csv('data/div1.csv', header=False, index=False)