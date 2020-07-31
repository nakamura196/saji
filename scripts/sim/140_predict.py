from annoy import AnnoyIndex
import glob
from os.path import join
import numpy
import os
import json
import yaml
import argparse    # 1. argparseをインポート

############

skip_flg = False

############

# 次元
dims = 2048

# 検索対象数
n_nearest_neighbors = 200
n_nearest_neighbors = n_nearest_neighbors + 1

t = AnnoyIndex(dims, metric='angular')
t.load('data/index.ann')

# インデックスマップの読み込み（Annoyのインデックス内のIDと特徴ベクトルの対応）

map_path = "data/file_index_map.json"
file_index_map = {}
max = 0
with open(map_path) as f:
    data = json.load(f)
    index_id_map = {}
    id_index_map = {}
    for index in data:
        index_id_map[int(index)] = data[index]
        id_index_map[data[index]] = int(index)
        max += 1

print(id_index_map)
# 予測

count = 0
for id in sorted(id_index_map):

    count += 1
    print(str(count)+"/" + str(max) + "\t" + id)

    dir = "data/json/similar_images"
    os.makedirs(dir, exist_ok=True)

    opath = dir + "/" + id + ".json"
    if os.path.exists(opath) and skip_flg:
        continue

    query_index = id_index_map[id]
    nearest_neighbors = t.get_nns_by_item(
        query_index, n_nearest_neighbors, include_distances=False)  # True)

    indexes = nearest_neighbors  # [0]

    # scores = nearest_neighbors[1]

    similar_images = []

    for i in range(0, len(indexes)):

        target_index = indexes[i]

        target_id = index_id_map[target_index]

        if id != target_id:
            similar_images.append(target_id)

    fw = open(opath, 'w')
    json.dump(similar_images, fw, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
