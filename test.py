#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


def print_cluster(near_list):
    for c in near_list:
        print("nodes:" + str(c[1].cluster.nodes) + "  nears:" + str(c[1].near_cluster.nodes) +
              "  dist:" + str(c[1].distance))


# クラスタクラス
# ノードリストのみ保有する
class Cluster:
    def __init__(self, node):
        self.nodes = []
        self.nodes.append(node)

    def marge(self, cluster):
        self.nodes.extend(cluster.nodes)

    def calc_dist(self, graph, cluster):
        counter = 0
        sum_dist = 0
        for target_node in cluster.nodes:
            for source_node in self.nodes:
                # source -> target
                if not nx.has_path(graph, source=source_node, target=target_node):
                    sum_dist += 1000
                else:
                    path = nx.shortest_path(graph, source=source_node, target=target_node)
                    sum_dist += len(path) - 1

                # target -> source
                if not nx.has_path(graph, source=target_node, target=source_node):
                    sum_dist += 1000
                else:
                    path = nx.shortest_path(graph, source=target_node, target=source_node)
                    sum_dist += len(path) - 1

                counter += 1
        return sum_dist / counter

    def find_near_cluster(self, graph, target_list):
        minimum = 10000
        near = None
        for c in target_list:
            # 同じノードは飛ばす
            if self == c:
                continue

            # 距離を計算して最短かチェック
            dist = self.calc_dist(g, c)
            if dist < minimum:
                minimum = dist
                near = c

        # 最短のクラスタを保持
        return Near(self, near, minimum)


class Near:
    def __init__(self, c, near, dist):
        self.cluster = c
        self.near_cluster = near
        self.distance = dist


# クラスタ数
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
dist_list = {}
users = (1,2,3,4,5,6)
for user in users:
    c = Cluster(user)
    dist_list[c] = Near(c, None, 10000)

# 初期の距離計算
for c in dist_list.keys():
    # 最短のクラスタを保持
    dist_list[c] = c.find_near_cluster(g, dist_list.keys())

min_cluster = min(dist_list.items(), key=lambda x: x[1].distance)

while len(dist_list) > cluster_num:
    print ("■□:::marge:::□■")
    marge_cluster = min_cluster[1].cluster
    near_cluster = min_cluster[1].near_cluster
    print_cluster(dist_list.items())
    print("↑bef   ↓aft")
    dist_list.pop(near_cluster)
    marge_cluster.marge (near_cluster)
    print_cluster(dist_list.items())

    # マージしたクラスタの距離を再計算
    dist_list[marge_cluster] = marge_cluster.find_near_cluster(g, dist_list.keys())
    min_cluster = min(dist_list.items(), key=lambda x: x[1].distance)

    # マージしたクラスタに最も近いクラスタを再計算
    for c in dist_list.items():
        if c[1].near_cluster == near_cluster:
            dist_list[c[1].cluster] = c[1].cluster.find_near_cluster(g, dist_list.keys())
