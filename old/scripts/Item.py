import bs4
import json
import requests
import os
import pprint
import copy
import hashlib

class Item:
    soup = None

    skip = False
    
    dirname = "tei_mod"
    uri_prefix = "https://nakamura196.github.io/saji"
    
    dict4div1 = {}
    dict4div2item = {}
    hutime = {}

    # 不具合の保存用
    dateErrors = {}
    missingTypes = set()
    # missingTypes2 = set()
    
    item = {
        
        "children": [],
        "metadata": {
            "element": "item",
        }
        # "note" : []
    }
    
    def __init__(self, file):
        # 初期化

        self.dateErrors = {}
        self.missingTypes = set()

        soup = bs4.BeautifulSoup(open(file), 'xml')

        title = file.split("/")[-1].split(".")[0]

        if title in ["DSCN0467", "DSCN1687", "DSCN0394", "DSCN8912", "DSCN1910", "DSCN0885"]:
            self.skip = True
        
        self.item["metadata"]["title"] = title
        
        self.soup = soup
        # self.dict4div1 = getDict4div1()
        
        with open('../docs/etc/dict.json', encoding="utf8") as f:
            map = {}
            df = json.load(f)
            for key in df:
                map[key.lower()] = df[key].lower()
            self.dict4div1= map

        self.getDict4div2item()
            
        # これは後の方がよい？
        self.getCanvases()

        self.getHutime()

    @staticmethod
    def staticGetHutime(path):
        import pandas as pd
        df = pd.read_csv(path)
        map = {}
        for index, row in df.iterrows():
            key = row["row"]
            value = row["hutime"]
            
            map[key] = value
        return map

    @staticmethod
    def staticConvertDate(date, hutime):
        print(date)
        date2 = copy.copy(date)
        attrs = date.attrs

        '''
        for attr in attrs:
            if attr == "when-custom":
                date2["when"] = 
            print(attr, date[attr])
        '''

        '''
        import pandas as pd
        df = pd.read_csv(path)
        map = {}
        for index, row in df.iterrows():
            key = row["row"]
            value = row["hutime"]
            
            map[key] = value
        return map
        '''

    @staticmethod
    def staticConvertDate2(value, hutime):

        if value in hutime:
            return hutime[value]

        flg = True

        while flg:

            # time.sleep(1)
            url = "http://ap.hutime.org/cal/?ival="+value+"&ical=103.1&method=conv&ep=b&ocal=101.1&otype=date&oprop=text&oform=gg%20YYYY-MM-dd"

            # print(url)
            r = requests.get(url)
            sd = r.text.replace("C.E. ", "").strip()

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

        return sd

    @staticmethod
    def formatDate(date):
        dd = date.split("-")

        hd2 = None
        
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

        if not hd2:
            return None

         # convert後のチェック
        year = int(hd2.split("-")[0])
        if year > 2000 or year < 1000:
            return None

        return hd2

    def getHutime(self):
        import pandas as pd
        df = pd.read_csv('data/hutime.csv')
        map = {}
        for index, row in df.iterrows():
            key = row["row"]
            value = row["hutime"]
            
            map[key] = value

        self.hutime = map

    def getDict4div2item(self):
        import pandas as pd
        df = pd.read_csv('data/map4div2item.csv')
        map = {}
        for index, row in df.iterrows():
            '''
            value = row["まとめ"]
            if pd.isnull(value):
                continue
            div1s = sorted(list(set(row["tei:div1_formatted"].lower().split("|"))))
            div1 = "|".join(div1s)
            
            map[div1] = value.lower()
            '''
            map[row["type"]] = row["type_formatted"]

        self.dict4div2item = map

        # pprint.pprint(map)
            
    def getValueAndAttrs(self, e):
        item = {
            "text": e.text
        }
        
        map = e.attrs
        
        for key in map:
            item[key] = map[key]
            
        return item
    
    def extractElements(self, div, type):
        values = []
        if not div:
            return values
        metadata= div.find_all(type)
        for value in metadata:
            # self.metadata[type].append(value.text)
            values.append(self.getValueAndAttrs(value))
        return values

    def attachDate(self):
        self.item["metadata"]["date"] = self.extractDates(self.soup)
            
    def extractDates(self, div):
        values = []
        metadata= div.find_all("date")
        for value in metadata:
            item = {
                "value" : value.text
            }
            
            '''
            if value.get("when-custom"):
                item["when-custom"] 
            wc = value.get("when-custom")
            print("wc", wc)
            if wc:
                self.metadata["date"].append(wc)
            '''
            
            map = value.attrs
            
            for key in map:
                item[key] = map[key]
                    
            values.append(item)
        return values

    def attachCreated(self):
        created = self.extractCreated(self.item["metadata"]["date"])
        self.item["metadata"]["created"] = created

    def extractCreated(self, dates):

        created = "0000-00-00"

        hutime = self.hutime

        for date in dates:
            if date.get("type") == "created":

                value = None

                attr = None

                title = self.item["metadata"]["title"]
                

                if date.get("when"):
                    value = date.get("when")
                elif date.get("from"):
                    value = date.get("from")
                elif date.get("to"):
                    value = date.get("from")
                else:
                    error = copy.deepcopy(date)
                    error["reason"] = "不具合あり"
                    hash = hashlib.md5(json.dumps(error).encode()).hexdigest()
                    self.dateErrors[hash] = error

                if value and value > created:
                    created = value

        if created == "0000-00-00":
            created = "2050-12-30"
        
        return created
                
    def extractCerts(self, div):
        values = []
        metadata= div.find_all("date")
        for value in metadata:
            if value.get("cert"):
                value = "date_cert_" + value.get("cert")
                # self.metadata.cert.append(value)
                values.append(value.strip())
                
        return values
            
    def extractDivs(self):
        self.item["children"] = self.extractDiv1s()
            
    def extractDiv1s(self):
        children = []
        divs = self.soup.find_all("div1")
        for div in divs:
            if div.get("type"):
                value = div.get("type")
                element = "div1"
                
                div_new = {
                    "metadata" : {
                        "element" : element,
                        "type": value,
                        "type_formatted": self.getFormattedType(value),
                        
                        "fulltext" : self.extractFullText(div),
                        "cert" : self.extractCerts(div),
                        "date" : self.extractDates(div),
                        "persName": self.extractElements(div, "persName"),
                        "placeName": self.extractElements(div, "placeName"),
                        "title": self.extractDivTitle(div, element),
                    },
                    "children" : self.extractDiv2s(div),
                }
                div_new["metadata"]["created"] = self.extractCreated(div_new["metadata"]["date"])
                
                # 画像情報の取得
                imageInfo = self.extractImageInfo(div)
                for key in imageInfo:
                    div_new[key] = imageInfo[key]
                
                children.append(div_new)
        return children

    def attachFormattedType(self):
        div1s = self.item["children"]
        types = set()
        for div1 in div1s:
            types.add(div1["metadata"]["type_formatted"])

        types_str = "|".join(sorted(list(types)))

        types_str_formatted = None

        if types_str in self.dict4div2item:
            types_str_formatted = self.dict4div2item[types_str]
        else:
            types_str_formatted = "[Missing I] " + types_str

        self.item["metadata"]["type_formatted"] = types_str_formatted
        
    
    def getFormattedType(self, value):
        for key in self.dict4div1:
            '''
            if key in value.lower():
                return self.dict4div1[key]
            '''
            if key == value.lower():
                return self.dict4div1[key]

        # print("[Missing D] "+value.lower())
        # 変換できなかったtype
        self.missingTypes.add(value.lower())
            
        return "[Missing D] "+value.lower()
                
    def extractDiv2s(self, div_):
        children = []
        divs = div_.find_all("div2")
        for div in divs:
            if div.get("type"):
                element = "div2"
                value = div.get("type")
                div_new = {
                    "metadata" : {
                        "element" : element,
                        "type": value,
                        "type_formatted": self.getFormattedType(value),
                        
                        
                        
                        "fulltext" : self.extractFullText(div),
                        "cert" : self.extractCerts(div),
                        "date" : self.extractDates(div),
                        "persName": self.extractElements(div, "persName"),
                        "placeName": self.extractElements(div, "placeName"),
                        "title": self.extractDivTitle(div, element)
                    },
                    "children" :self.extractDiv3s(div),
                }
                div_new["metadata"]["created"] = self.extractCreated(div_new["metadata"]["date"])
                
                imageInfo = self.extractImageInfo(div)
                for key in imageInfo:
                    div_new[key] = imageInfo[key]
                
                children.append(div_new)
        return children

    def extractDivTitle(self, div, type):
        id = "None"
        if div.get("facs"):
            id = div.get("facs").replace("#", "")
        return self.item["metadata"]["title"] + "-" + type + "-" + id
    
    def extractDiv3s(self, div_):
        children = []
        divs = div_.find_all("div3")
        for div in divs:
            if div.get("type"):
                value = div.get("type")
                element = "div3"
                div_new = {
                    "metadata" : {
                        "element" : element,
                        "type": value,
                        "type_formatted": self.getFormattedType(value),
                        "fulltext" : self.extractFullText(div),
                        "cert" : self.extractCerts(div),
                        "date" : self.extractDates(div),
                        "persName": self.extractElements(div, "persName"),
                        "placeName": self.extractElements(div, "placeName"),
                        "title": self.extractDivTitle(div, element)
                    }
                    
                }
                div_new["metadata"]["created"] = self.extractCreated(div_new["metadata"]["date"])
                
                imageInfo = self.extractImageInfo(div)
                for key in imageInfo:
                    div_new[key] = imageInfo[key]
                
                children.append(div_new)
        return children
    
    def extractNotes(self):
        notesStmt = self.soup.find("notesStmt")
        values = self.extractElements(notesStmt, "note")
        self.item["metadata"]["note"] = values
        
    def attachFullText(self):
        self.item["metadata"]["fulltext"] = self.extractFullText(self.soup)
                
    def extractFullText(self, div):
        fulltext = div.text.strip() # .replace("\n", " ").strip()
        return fulltext
    
    '''
    def extractFullText_org(self, div=self.soup):
        fulltext = self.soup.text.replace("\n", " ").strip()
        self.metadata["fulltext"] = fulltext
    '''
    
    def getCanvases(self):
        
        manifest = self.soup.find("surfaceGrp").get("facs")
        
        id = manifest.split("/")[-2]
        
        file = "../docs/iiif/" + id + "/manifest.json"
        
        if not os.path.exists(file):
        
            df = requests.get(manifest).json()
            
            fw = open(file, 'w')
            json.dump(df, fw, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))
            fw.close()
            
        with open(file) as f:
            df = json.load(f)
            
        canvases = df["sequences"][0]["canvases"]
        
        map = {}
        for i in range(len(canvases)):
            canvas = canvases[i]
            map[canvas['@id']] = canvas["images"][0]["resource"]["service"]["@id"]
            
            if i == 0:
                self.item["canvas"] = canvas["@id"]
        self.canvases = map
        
        # 以下、重複。要検討。
        self.manifest =  manifest
        self.item["manifest"] = manifest
        
    def extractMedia(self):
        self.item["thumbnail"] = self.soup.find("graphic").get("url").replace("/original/", "/medium/")
        self.item["tei_url"] = self.uri_prefix + "/"+ self.dirname+"/" + self.item["metadata"]["title"] + ".xml"
        
    def extractSourceDesc(self):
        sourceDesc = self.soup.find("sourceDesc").find("p")
        # print(sourceDesc.text)
        try:
            metadata_json = json.loads(sourceDesc.text)
            for field in metadata_json:
                value_array = metadata_json[field]
                field_fixed = field.replace("saji:", "")
                self.item["metadata"][field_fixed] = value_array
        except Exception as e:
            print("sourceDescの処理エラー", e)
            
    def extractImageInfo(self, div):
        facs_id = div.get("facs")
        
        if not facs_id:
            return {}
        
        facs_ids = facs_id.replace("#", "").split(" ")
        
        # 二つのIDの場合、どうするか
        
        for facs_id in facs_ids:
            
            # 入力ミスにより、空の場合あり
            if facs_id == "":
                continue
        
            zone = self.soup.find(attrs={"xml:id" : facs_id})
            
            # zoneがない場合が存在します。
            if not zone:
                continue

            surface = zone.parent

            graphic = surface.find("graphic")

            canvas_uri = graphic.get("n")

            # print(zone)

            ulx = int(zone.get("ulx"))
            uly = int(zone.get("uly"))
            lrx = int(zone.get("lrx"))
            lry = int(zone.get("lry"))

            x = ulx
            y = uly

            w = lrx - x
            h = lry - y

            member_id = canvas_uri + "#xywh=" + str(x) + ","+str(y)+","+str(w)+","+str(h)

            canvases = self.canvases

            image = canvases[canvas_uri] + "/{},{},{},{}/200,/0/default.jpg".format(x, y, w, h)

            return {
                "thumbnail" : image,
                "member" : member_id,
                "canvas" : canvas_uri,
                # "manifest": self.manifest
            }
        
        return {}
        
            
    def convert2json(self):
        return self.item
    
    @staticmethod
    def getDateValue(_date):
        """
        dateノードのValueの取得

        Parameters
        --------------
        date : xml element

        Returns
        -------
        dateValue : string
            XXXX-XX-XXの形の日付文字列

        """

        dateValue = None

        if _date.get("when-custom"):
            dateValue = _date.get("when-custom")
        elif _date.get("from-custom"):
            dateValue = _date.get("from-custom")
        elif _date.get("to-custom"):
            dateValue = _date.get("to-custom")

        return dateValue
    
    @staticmethod
    def getDateType(_date):
        """
        dateノードのタイプの取得

        Parameters
        --------------
        date : xml element

        Returns
        -------
        n_type : string
            ノードのタイプ。when, from, toなど。

        """

        type = None

        if _date.get("when-custom"):
            type = "when"
        elif _date.get("from-custom"):
            type = "from"
        elif _date.get("to-custom"):
            type = "to"

        return type
    
    @staticmethod
    def getDataValueAndType(_date):
            return getDateValue(_date), getDateType(_date)