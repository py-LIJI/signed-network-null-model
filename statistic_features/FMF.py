# -*- coding: utf-8 -*-
"""
FMF
(节点正负度之差)
"""


import numpy as np
import networkx as nx


def dedivide_network_M(G):
    '''将原始网络分成正边网络和负边网络
      （分别包含原始网络全部节点）
    输入：G原始网络
    输出：Gp正边网络（含所有节点）
         Gn负边网络（含所有节点）
    '''
    
    edge_list = []  # 边数据容器（非字典）
    positive_edges = []  # 正边数据容器
    negative_edges = []  # 负边数据容器
    
    for i, j, weight_data in G.edges(data = True):
        # 消除权值字典结构
        if 'weight' in weight_data:
            edge_list.append([i, j, weight_data['weight']])     
    
    for item in edge_list:
        if item[2] == 1:       
            positive_edges.append(item)
            # M_pos=len(positive_edges)            
        elif item[2] == 2:       
            negative_edges.append(item)
            # M_neg=len(negitive_edges)
    
    # 正边网络                   
    Gp = nx.Graph()
    Gp.add_weighted_edges_from(positive_edges)
    # 负边网络
    Gn = nx.Graph()
    Gn.add_weighted_edges_from(negative_edges)
    
    # 使负边网络包含原始网络所有节点
    for i in Gp:
        if i in Gn.nodes():
            pass
        else:
            Gn.add_node(i)  
    
    # 使正边网络包含原始网络所有节点        
    for j in Gn:
        if j in Gp.nodes():
            pass
        else:
            Gp.add_node(j)             

    return Gp,Gn


def FMF(pos_degree, neg_degree):
    '''计算FMF（节点正负度之差）
    输入：pos_degree 节点正度值容器
         pos_degree 节点负度值容器
    输出：minus 节点FMF值数组
    '''
    
    a = []  # 节点正度值列表
    b = []  # 节点负度值列表
    
    for i in pos_degree:
        a.append(i[1])
    for j in neg_degree:
        b.append(j[1])        

    a_a = np.array(a)  # 节点正度值数组
    b_a = np.array(b)  # 节点负度值数组

    minus = a_a-b_a  # 节点FMF值数组
    
    return minus


def minus_dis(Gp,Gn):
    '''计算原网络节点FMF取值情况列表（排序后）
       与取该FMF值的节点个数占总节点个数的比例
      输入：Gp 正边网络（所有节点）
           Gn 负边网络（所有节点）
      输出：x 节点FMF取值情况列表（排序后）
           y 取该FMF值的节点个数占总节点个数的比例
    '''
    
    pos_degree = Gp.degree()  # 节点正度值字典
    neg_degree = Gn.degree()  # 节点负度值字典
    
    # 解除字典结构并排序
    pos_degree_new = list(sorted(pos_degree, key = lambda pos_degree: pos_degree[0]))
    neg_degree_new = list(sorted(neg_degree, key = lambda neg_degree: neg_degree[0]))

    minus = FMF(pos_degree_new, neg_degree_new)
    x = list(set(list(minus)))
    x.sort()
    y=[]
    
    for i in x:
        y.append(list(minus).count(i)/len(list(minus)))
             
    return x, y


# 生成原网络
G = nx.read_edgelist('C://Users//Administrator//Desktop//statistic_features//N46edge.txt', 
                     nodetype = int, data = (('weight', float),))
# 将原网络划分成包含所有节点的正边网络和负边网络
Gp,Gn=dedivide_network_M(G)
# 计算节点FMF值，及取该值节点所占比例
x,y=minus_dis(Gp,Gn)












