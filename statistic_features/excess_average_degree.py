# -*- coding: utf-8 -*-
"""
余平均度
"""


import networkx as nx


def divide_network(G):
    '''将原始网络G拆成正边网络或负边网络（无孤立节点）
    输入：G 原始网络
    输出：Gp 正边网络（无孤立节点）
         Gn 负边网络（无孤立节点）
    '''
    
    edge_list = []
   
    for i, j, weight_data in G.edges(data = True):
        if 'weight' in weight_data:  # 排除孤立节点
            # 权重值去除字典结构  
            edge_list.append([i, j, weight_data['weight']])
            
    positive_edges = []  # 正边数据容器
    negitive_edges = []  # 负边数据容器
    
    for item in edge_list:
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


def knn_to_list(knn_dict):
    '''按升序分离度值与其对应的余平均度为列表
    输入：knn_dict {度值：其对应的余平均度}字典
    输出：knn_degrees 排序后的度值列表
         knn_values 排序后的余平均度列表
    '''
    
    list_keys = list(knn_dict)  # 字典键列表
    knn_list = []
    
    for item in list_keys:
        knn_list.append((int(item), knn_dict[item]))  #字典变元组
    
    # 以度值为比较对象，对其所在的元组排序     
    knn_list_new = sorted(knn_list, key=lambda knn_list : knn_list[0])    
    knn_degrees = []
    knn_values = []
    
    for item in knn_list_new:
        knn_degrees.append(item[0])  # 分离度值
        knn_values.append(item[1])  # 分离余平均度
    
    return knn_degrees, knn_values


# 生成原始网络G
G = nx.read_edgelist('C://Users//Administrator//Desktop//statistic_features//N46edge.txt', 
                     nodetype = int, data = (('weight',float),))
# 生成正边网络或负边网络（无孤立节点）
Gp, Gn = divide_network(G)
# 以字典的形式返回正边网络（无孤立节点）中所有度为K的节点的余平均度
knn_p0 = nx.k_nearest_neighbors(Gp)
# 以字典的形式返回负边网络（无孤立节点）中所有度为K的节点的余平均度
knn_n0 = nx.k_nearest_neighbors(Gn)
# 分离正边网络（无孤立节点）的度值与余平均度
knn_p0_degree, knn_p0_values = knn_to_list(knn_p0)
# 分离负边网络（无孤立节点）的度值与余平均度
knn_n0_degree, knn_n0_values = knn_to_list(knn_n0)


