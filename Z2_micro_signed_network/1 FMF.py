# -*- coding: utf-8 -*-
"""
FMF
(节点正负度之差)
"""

import numpy as np
import networkx as nx


def separate_network(G):
    '''将原始网络分成正边网络和负边网络
      （分别包含原始网络全部节点）
    输入：G原始网络
    输出：Gp正边网络（含所有节点）
         Gn负边网络（含所有节点）
    '''
    list_edge = []  # 边数据容器（非字典）
    positive_edge = []  # 正边数据容器
    negative_edge = []  # 负边数据容器

    for node_i, node_j, weight_data in G.edges(data=True):
        if 'weight' in weight_data:
            list_edge.append([node_i, node_j, weight_data['weight']])
        else:
            pass
    
    for i in list_edge:
        if i[2]==1:
            positive_edge.append(i)
        elif i[2]==2:
            negative_edge.append(i)
        else:
            pass
         
    Gp=nx.Graph()
    Gn=nx.Graph()
    Gp.add_weighted_edges_from(positive_edge)
    Gn.add_weighted_edges_from(negative_edge)
    
    # 包含原始网络全部节点
    for i in Gp.nodes():
        if i in Gn.nodes():
            pass
        else:
            Gn.add_node(i)
            
    for j in Gn.nodes():
        if j in Gp.nodes():
            pass
        else:
            Gp.add_node(j)
            
    return Gn,Gp


def FMF(Gn, Gp):
    '''计算FMF（节点正负度之差）
     输入：Gp 正边网络（所有节点）
           Gn 负边网络（所有节点）
     输出：diff 节点FMF取值情况列表（排序后）
    '''
    positive_degree=Gp.degree()
    negative_degree=Gn.degree()
    sort_positive_degree=list(sorted(positive_degree, key= lambda positive_degree: positive_degree[0]))
    sort_negative_degree=list(sorted(negative_degree, key= lambda negative_degree: negative_degree[0]))
    
    p_degree=[]  # 正度值容器
    n_degree=[]  # 负度值容器
    
    for i in sort_positive_degree:
        p_degree.append(i[1])
    for j in sort_negative_degree:
        n_degree.append(j[1])
       
    diff_degree=list(np.array(p_degree)-np.array(n_degree)) # 计算FMF
    
    diff_node=[]  # 对应节点容器
    for i in sort_positive_degree:
        diff_node.append(i[0])
    
    diff=dict(zip(diff_node, diff_degree))  # 节点及其对应的FMF值
    
    return diff



# 计算原始网络
G=nx.read_edgelist('N46edge.txt', nodetype=int, data=(('weight', float), ))
# 分离网络
Gn, Gp=separate_network(G)
# 计算节点及其对应的FMF值
diff=FMF(Gn, Gp)



















