import xml.etree.ElementTree as ET
import sys
import json
import argparse
import glob
import os
import requests

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)


dirname = "tei"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

for i in range(len(files)):

    file = files[i]

    print(str(i+1)+"/"+str(len(files))+"\t"+file)

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(file)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    surfaces = root.findall(prefix+"surface")

    for surface in surfaces:
        graphics = surface.findall(prefix+"graphic")
        for graphic in graphics:
            url = graphic.get("url")
            filename = url.split("/")[-1]
            opath = "../images/"+filename 
            if not os.path.exists(opath):
                download_img(url, opath)