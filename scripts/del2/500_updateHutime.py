from Item import Item
import glob
from tqdm import tqdm
import copy
import json
import pprint
import requests
import time
from tqdm import tqdm
import pandas as pd

converts = {}

def get_hutime(hd2):

    if hd2 in converts:
        return converts[hd2]

    # time.sleep(1)
    url = "http://ap.hutime.org/cal/?ival="+hd2+"&ical=103.1&method=conv&ep=b&ocal=101.1&otype=date&oprop=text&oform=gg%20YYYY-MM-dd"

    # print(url)
    r = requests.get(url)
    sd = r.text.replace("C.E. ", "").strip()

    converts[hd2] = sd

    return sd

def conv_date(date):
    dd = date.split("-")

    hd2 = "unknown"
    
    l = len(dd)
    if l == 1:
        year = dd[0]
        if year.isdecimal():
            hd2 = year + "-12-29"
    elif l == 2:
        
        year = dd[0]
        month = dd[1]
        if year.isdecimal() and month.isdecimal():
            hd2 = year+"-"+month+"-29"
    elif l == 3:
        year = dd[0]
        month = "12" if dd[1].strip() == "" else dd[1].strip()
        day = "29" if dd[2].strip() == "" else dd[2].strip()
        if year.isdecimal() and month.isdecimal() and day.isdecimal():
            hd2 = year + "-" + month + "-" + day

    return hd2

hutime_path = 'data/hutime.csv'

'''
with open('data/hutime.json') as f:
    hutime = json.load(f)
'''

import pandas as pd
df = pd.read_csv(hutime_path)
hutime = {}
for index, row in df.iterrows():
    sd = row[2]
    year = int(sd.split("-")[0])
    if year > 1000 and year < 2000:
        hutime[row[0]] = row

with open('data/items.json') as f:
    df = json.load(f)

keys = set()

attrs = ["when-custom", "from-custom", "to-custom"]

for item in df:
    dates = item["date"]

    for date in dates:
        for attr in attrs:
            if attr in date:
                keys.add(date[attr])


keys = list(sorted(keys))

for key in tqdm(keys):
    # continue
    if key in hutime:
        continue

    hd2 = conv_date(key)
    if hd2 != "unknown":
        
        # convert後のチェック
        year = int(hd2.split("-")[0])
        if year > 2000 or year < 1000:
            continue

        flg = True

        while flg:
        
            sd = get_hutime(hd2) 

            year = int(sd.split("-")[0])

            if year < 1000:
                # 一日前
                spl = hd2.split("-")

                try:
                    hd2 = "{}-{}-{}".format(spl[0], spl[1], int(spl[2]) - 1)
                except:
                    sd = None
                    flg = False
            elif year > 2000:
                sd = None
                flg = False
            else:
                flg = False

        if sd:
            hutime[key] = [key, hd2, sd]
        
rows = []
rows.append(["row", "converted", "hutime"])
for key in hutime:
    rows.append(hutime[key])

df = pd.DataFrame(rows)
df.to_csv(hutime_path, header=False, index=False)