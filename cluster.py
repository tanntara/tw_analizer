#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


# クラスタクラス
# ノードリストのみ保有する
class Cluster:
    def __init__(self, node):
        self.nodes = []
        self.nodes.append(node)

    def marge(self, cluster):
        self.nodes.extend(cluster.nodes)

    def calc_dist(self, graph, cluster):
        return 1


cluster_num = 2

g = nx.DiGraph()
edges = [
    (1, 4),
    (1, 2),
    (2, 3),
    (3, 1),
    (4, 5),
    (5, 6),
    (6, 4)
]

g.add_edges_from(edges)

users = []

# クラスタリストを初期化する
cluster_list = []
users = (1,2,3,4,5,6)
for user in users:
    c = Cluster(user)
    cluster_list.append(c)

dist_list = {}
for c in cluster_list:
    min_dist = 1000
    near_cluster = None

    for temp_c in cluster_list:
        # 同じノードは飛ばす
        if c == temp_c:
            continue

        # 距離を計算して最短かチェック
        dist = c.calc_dist(g, temp_c)
        if dist < min_dist:
            min_dist = dist
            near_cluster = temp_c

    # 最短のクラスタを保持
    dist_list[c] = (near_cluster, min_dist)

min = min(dist_list.items(), key=lambda x: x[1][1])
print(min[0].nodes[0])
print(min[1][0].nodes[0])
print(min[1][1])

