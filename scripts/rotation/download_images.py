import csv
import urllib.request  # ライブラリを取り込む
import os

f = open('data/media.csv', 'r')

folder = "medium"

reader = csv.reader(f)
header = next(reader)

count = 0

for row in reader:
    id = row[7]
    print(id)

    count += 1

    if count % 20 == 0:
        print(count)

    save_name = folder+"/"+id+".jpg"  # test1.pngという名前で保存される。

    if not os.path.exists(save_name):

        url = "https://diyhistory.org/public/phr2/files/"+folder+"/"+id+".jpg"

        
        

        # ダウンロードを実行
        urllib.request.urlretrieve(url, save_name)

f.close()
