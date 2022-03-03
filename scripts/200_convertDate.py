
import sys
import urllib
import json
import argparse
import urllib.request
import glob
import requests
import bs4
from Item import Item
import copy
from tqdm import tqdm

dirname = "tei3"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

path = "../docs/data"

hutime = Item.staticGetHutime('data/hutime.csv')

for l in tqdm(range(len(files))):
    file = files[l]

    soup = bs4.BeautifulSoup(open(file), 'xml')

    texts = soup.find_all("text")

    for text in texts:

        dates = text.find_all("date")
        for i in range(len(dates)):
            date = dates[i]

            date2 = copy.copy(date)
            attrs = date.attrs
            for attr in attrs:
                value = attrs[attr]

                # フォーマット
                bvalue = Item.formatDate(value)
                if not bvalue:
                    continue
                
                if attr == "when-custom":
                    del date2["when"]
                    avalue = Item.staticConvertDate2(bvalue, hutime)
                    if value:
                        date2["when"] = avalue
                        hutime[bvalue] = avalue
                if attr == "from-custom":
                    del date2["from"]
                    avalue = Item.staticConvertDate2(bvalue, hutime)
                    if value:
                        date2["from"] = avalue
                        hutime[bvalue] = avalue
                if attr == "to-custom":
                    del date2["to"]
                    avalue = Item.staticConvertDate2(bvalue, hutime)
                    if value:
                        date2["to"] = avalue
                        hutime[bvalue] = avalue

            attrs2 = date2.attrs
            for attr in attrs2:
                date[attr] = attrs2[attr]

    with open(file.replace("tei3", "tei_mod"), "w") as file2:
        file2.write(str(soup))