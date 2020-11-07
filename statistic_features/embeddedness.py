# -*- coding: utf-8 -*-
"""
嵌入性
"""


import networkx as nx


def divide_network(G):
    '''将原始网络分别划分为正边网络和负边网络
    输入：G 原始网络
    输出：Gp正边网络
         Gn负边网络
    '''
    
    edge_list = []  # 创建原始网络数据容器
    
    for i, j, weight_data in G.edges(data = True):
        if 'weight' in weight_data:
            # 解除权值字典格式
            edge_list.append([i, j, weight_data['weight']])
             
    positive_edges = []  # 创建正边数据容器
    negitive_edges = []  # 创建负边数据容器
    
    for item in edge_list:
        # 根据权值将正负边数据分别归属到各自容器内
        if item[2] == 1:       
            positive_edges.append(item)
        if item[2] == 2:       
            negitive_edges.append(item)
        
    Gp = nx.Graph()  # 生成正边网络
    Gp.add_weighted_edges_from(positive_edges)
        
    Gn = nx.Graph()  # 生成负边网络
    Gn.add_weighted_edges_from(negitive_edges)
    
    return Gp, Gn


def CommonNeighbor(G, nodeij):
    '''求取节点i,j的共同邻居节点的个数（嵌入性）
    输入：G 对象网络
          nodeij 边数据
    输出：num_cn 共同邻居节点个数
    '''
    
    node_i = nodeij[0]  # 由边获取节点i
    node_j = nodeij[1]  # 由边获取节点j
    # 获取节点i的邻居节点生成器
    neigh_i = set(G.neighbors(node_i))  
    # 获取节点j的邻居节点生成器
    neigh_j = set(G.neighbors(node_j))
    # 获取节点i,j的共同邻居节点生成器
    neigh_ij = neigh_i.intersection(neigh_j)
    # 获取数量
    num_cn = len(neigh_ij)       
    
    return num_cn


def CN_embedding(G, Gpn):
    
    CN_list = []
    # 捕获可能的错误信息
    for item in G.edges():
        try:
            item_CN = CommonNeighbor(Gpn, item)
            # 获取由节点i,j的共同邻居节点数量和两者连边符号列表
            CN_list.append((item_CN, G[item[0]][item[1]]['weight']))
        except:
            pass
    
    # 对共同邻居节点数量进行排序
    CN_list_sort = sorted(CN_list, key=lambda CN_list: CN_list[0])
    degree_list = []
    positive_edge_cn = []
    # 正边两节点没有共同邻居节点的边数
    positve_edge_number = 0
    # 原始网络中 
    sum_edge_number = 0
    item_index = 0
    
    for item in CN_list_sort:
        if item[0] == item_index:
            if item[1] == 1:
                positve_edge_number = positve_edge_number+1
            sum_edge_number = sum_edge_number+1
        elif item[0] > item_index:
            if sum_edge_number == 0:
                degree_list.append(item_index)
                positive_edge_cn.append(0)
            else:  
                degree_list.append(item_index)
                positive_edge_cn.append(float(positve_edge_number)/sum_edge_number)
            item_index = item[0]
            positve_edge_number = 0
            sum_edge_number = 0
    
    return degree_list, positive_edge_cn


# 生成原始网络G
G = nx.read_edgelist('C://Users//Administrator//Desktop//statistic_features//N46edge.txt', 
                     nodetype=int, data=(('weight', float),))
# 将原始网络分成正边网络和负边网络
Gp, Gn = divide_network(G)
degree_list_p0, positive_edge_cn_p0 = CN_embedding(G, Gp)
degree_list_n0, positive_edge_cn_n0 = CN_embedding(G, Gn)





