import json

with open('data/items.json') as f:
    df = json.load(f)

selections = []
for item in df:
    members = []
    manifest = item["manifest"]
    selection = {
        "@id": "https://nakamura196.github.io/saji/data/curation.json/range1",
        "@type": "sc:Range",
        "label": "Automatic curation by TEI",
        "members": members,
        "within" : {
            "label" : item["title"],
            "@type" : "sc:Manifest",
            "@id" : manifest
        }
    }
    
    # print(item["title"])
    
    related = "https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url=" + item["tei_url"]
    
    div1s = item["children"]

    fond = item["fond"]
    
    for div1 in div1s:
        
        if "member" in div1:
        
            member1 = {
                "label": div1["title"],
                "@type": "sc:Canvas",
                "@id": div1["member"],
                "metadata": [
                   {
                       "label": "type",
                       "value": div1["type"]
                   },
                    {
                       "label": "type_formatted",
                       "value": div1["type_formatted"]
                   },
                    {
                       "label": "element",
                       "value": div1["element"]
                   },
                   {
                       "label": "created",
                       "value": div1["created"]
                   },
                   {
                       "label": "fond",
                       "value": fond
                   },
                    {
                        "label": "title",
                        "value": div1["title"]
                    }
                ],
                "thumbnail": div1["thumbnail"],
                "related ": related 
            }
            members.append(member1)
        
        div2s = div1["children"]
        
        for div2 in div2s:
            div3s = div2["children"]
            
            for div3 in div3s:
                member3 = {
                    
                }
                # members.append(member3)
    
    
    member = {
        "label": item["title"],
        "@type": "sc:Canvas",
        "@id": item["canvas"],
        "metadata": [
           {
               "label": "element",
               "value": item["element"]
           },
            {
                "label": "created",
                "value": item["created"]
            },
            {
                "label": "fond",
                "value": fond
            },
            {
                "label": "type_formatted",
                "value": item["type_formatted"]
            },
            {
                "label": "title",
                "value": item["title"]
            }
        ],
        "thumbnail": item["thumbnail"],
        "related": related
    }
    members.append(member)
    
    
    selections.append(selection)
    
curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "https://nakamura196.github.io/saji/data/curation2.json",
    "@type": "cr:Curation",
    "selections" : selections,
    "label": "オスマン・トルコ語文書群のデータ整理"
}

fw = open("../docs/data/curation2.json", 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
fw.close()

fw = open("../docs/data/curation2.min.json", 'w')
json.dump(curation, fw)
fw.close()