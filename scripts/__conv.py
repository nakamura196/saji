import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
import glob
from bs4 import BeautifulSoup
import requests
import json

dirname = "tei"
dir = "../docs/"+dirname
files = glob.glob(dir+"/*.xml")

for i in range(len(files)):
    file = files[i]

    soup = BeautifulSoup(open(file,'r'), 'xml')

    divs = soup.find_all("div")
    for div in divs:
        type =  div.get("type")
        if type:
            text = str(div)
            if "stamp" in type:
                text = text.replace("div", "div3")
                div.replaceWith(BeautifulSoup(text, "html.parser"))


    divs = soup.find_all("div")
    for div in divs:
        type =  div.get("type")
        if type:
            text = str(div)
            if "sign" in type:
                text = text.replace("<div ", "<div2 ").replace("</div>", "</div2>")
                div.replaceWith(BeautifulSoup(text, "html.parser"))

    divs = soup.find_all("div")
    for div in divs:
        type =  div.get("type")
        if type:
            text = str(div)
            text = text.replace("<div ", "<div1 ").replace("</div>", "</div1>")
            div.replaceWith(BeautifulSoup(text, "html.parser"))

    with open(file.replace("tei", "tei2"), "w") as file:
        file.write(str(soup).replace("xmlns:=", "xmlns="))