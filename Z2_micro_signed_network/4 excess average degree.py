# -*- coding: utf-8 -*-
"""
余平均度
excess average degree
"""

import networkx as nx


def seperate_network(G):
    '''将原始网络G拆成正边网络或负边网络（无孤立节点）
    输入：G 原始网络
    输出：Gp 正边网络（无孤立节点）
         Gn 负边网络（无孤立节点）
    '''
    
    list_edge = []
   
    for i, j, weight_data in G.edges(data = True):
        if 'weight' in weight_data:  # 排除孤立节点
            # 权重值去除字典结构  
            list_edge.append([i, j, weight_data['weight']])
            
    positive_edges = []  # 正边数据容器
    negitive_edges = []  # 负边数据容器
    
    for item in list_edge:
        if item[2] == 1:       
            positive_edges.append(item)
        if item[2] == 2:       
            negitive_edges.append(item)
    
    # 组成正边网络（无孤立节点）    
    Gp = nx.Graph()
    Gp.add_weighted_edges_from(positive_edges)  
    
    # 组成负边网络（无孤立节点）
    Gn = nx.Graph()
    Gn.add_weighted_edges_from(negitive_edges)
    
    return Gp, Gn

# 生成原始网络G
G = nx.read_edgelist('N46edge.txt', 
                     nodetype = int, data = (('weight',float),))
# 生成正边网络或负边网络（无孤立节点）
Gp, Gn = seperate_network(G)
# 以字典的形式返回正边网络（无孤立节点）中所有度为K的节点的余平均度
positive_knn = nx.k_nearest_neighbors(Gp)
# 以字典的形式返回负边网络（无孤立节点）中所有度为K的节点的余平均度
negative_knn = nx.k_nearest_neighbors(Gn)