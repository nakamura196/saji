import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json
import yaml

output_dir = "data/json"

print(output_dir)

# config
dims = 2048
# n_nearest_neighbors = 1000
trees = 100

t = AnnoyIndex(dims, metric='angular')

image_vectors_path = output_dir + "/image_vectors"
# files = glob.glob(image_vectors_path+"/[!d][!i]*.npy") #[!dig]
files = glob.glob(image_vectors_path+"/*.npy")
files = sorted(files)

map = {}

features = []

for file_index in range(len(files)):
    # print(file_index)

    file = files[file_index]

    if file_index % 500 == 0:
        print(str(file_index)+"\t"+str(len(files)), file)


    id = file.split("/")[-1].split(".")[0]

    # ターゲット設定
    source_id = id.split("-")[0]

    try:
        file_vector = numpy.load(files[file_index])
        t.add_item(file_index, file_vector)
        map[file_index] = id

        # features.append(file_vector)
    except:
        err = file
        print("err\t"+file)

t.build(trees)
t.save('data/index.ann') # モデルを保存することも可能です。

f2 = open('data/file_index_map.json', 'w')
json.dump(map, f2)

# numpy.save('data/features.npy', features)
