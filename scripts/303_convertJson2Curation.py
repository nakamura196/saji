import json

def getWhen(value):
    if "when" in value:
        return value["when"]
    elif "from" in value:
        return value["from"]
    else:
        return None

def getMetadata(metadata_org):
    metadata = []
    for key in metadata_org:

        value = metadata_org[key]

        if key == "note":
            values = {}
            
            for obj in value:

                key2 = "note-" + obj["type"] if "type" in obj else "note"
                if key2 not in values:
                    values[key2] = []
                values[key2].append(obj["text"])

            for key2 in values:
                metadata.append({
                    "label" : key2,
                    "value": values[key2]
                })

        else:

            # 日時
            if key == "date":
                values = []

                for obj in value:
                    whenValue = getWhen(obj)
                    if whenValue:
                        values.append(getWhen(obj))

                value = values

            metadata.append({
                "label" : key,
                "value": value
            })

    return metadata

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
            "label" : item["metadata"]["title"],
            "@type" : "sc:Manifest",
            "@id" : manifest
        }
    }
    
    # print(item["title"])
    
    related = "https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url=" + item["tei_url"]
    
    div1s = item["children"]

    fond = item["metadata"]["fond"]
    
    for div1 in div1s:
        
        if "member" in div1:

            metadata = getMetadata(div1["metadata"])
        
            member1 = {
                "label": div1["metadata"]["title"],
                "@type": "sc:Canvas",
                "@id": div1["member"],
                "metadata": metadata,
                "thumbnail": div1["thumbnail"],
                "related ": related 
            }
            members.append(member1)
        
        div2s = div1["children"]
        
        for div2 in div2s:

            if "member" in div2:

                metadata = getMetadata(div2["metadata"])
            
                member2 = {
                    "label": div2["metadata"]["title"],
                    "@type": "sc:Canvas",
                    "@id": div2["member"],
                    "metadata": metadata,
                    "thumbnail": div2["thumbnail"],
                    "related ": related 
                }
                members.append(member2)

            div3s = div2["children"]
            
            for div3 in div3s:
                if "member" in div3:
                    metadata = getMetadata(div3["metadata"])
                
                    member3 = {
                        "label": div3["metadata"]["title"],
                        "@type": "sc:Canvas",
                        "@id": div3["member"],
                        "metadata": metadata,
                        "thumbnail": div3["thumbnail"],
                        "related ": related 
                    }
                    members.append(member3)
    
    metadata = getMetadata(item["metadata"])
    
    member = {
        "label": item["metadata"]["title"],
        "@type": "sc:Canvas",
        "@id": item["canvas"],
        "metadata": metadata,
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