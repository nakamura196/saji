import json
import pandas as pd
import copy
import glob
import bs4
import os

files = glob.glob("../docs/tei_mod/*.xml")

for file in files:
    soup = bs4.BeautifulSoup(open(file), 'xml')
    texts = soup.find_all("text")

    if len(texts) > 1:

        base_title = os.path.splitext(os.path.basename(file))[0]

        for text in texts:

            n = text.get("n")

            title = base_title + "-" + str(n)
            
            soup_e = copy.copy(soup)
            es = soup_e.find_all('text')
            for e in es:
                e.decompose()

            soup_e.find("TEI").append(text)

            soup_e.find("title").replace_with(title)

            with open(file.replace("tei_mod", "tei_mod_spl").replace(base_title, title), "w") as file2:
                file2.write(str(soup_e))

    else:
        with open(file.replace("tei_mod", "tei_mod_spl"), "w") as file2:
            file2.write(str(soup))