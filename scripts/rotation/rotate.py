import csv
import urllib.request  # ライブラリを取り込む
import os
from PIL import Image

f = open('data/media.csv', 'r')

folder = "medium"
ofolder = "r_medium"

map = {}

reader = csv.reader(f)
header = next(reader)
for row in reader:
    filename = row[5]
    filename = filename.split("/")[-1]
    id = row[7]
    map[filename] = id

print(map)

f.close()


f = open('data/rotation.csv', 'r')

rotate = {}

reader = csv.reader(f)
header = next(reader)
for row in reader:
    filename = row[0]
    value = row[1]
    rotate[filename] = int(value)

print(rotate)

f.close()

for key in rotate:
    file = folder+"/"+map[key]+".jpg"
    print(file)
    output_path = file.replace(folder+"/", ofolder+"/")

    if os.path.exists(file) and not os.path.exists(output_path):

        im = Image.open(file)
        value = rotate[key]
        
        if value == 90:
            im_rotate = im.transpose(Image.ROTATE_270)
            im_rotate.save(output_path)
        elif value == 270:
            im_rotate = im.transpose(Image.ROTATE_90)
            im_rotate.save(output_path)
        elif value == 180:
            im_rotate = im.transpose(Image.ROTATE_180)
            im_rotate.save(output_path)
        # im_rotate = im.rotate(*(-1))
        

