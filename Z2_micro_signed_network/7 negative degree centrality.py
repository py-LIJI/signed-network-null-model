# -*- coding: utf-8 -*-
"""
负度中心性
negative degree centrality
"""

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


def negative_degree_centrality(Gn):
    '''计算负度中心性
     输入：Gp 正边网络（所有节点）
           Gn 负边网络（所有节点）
     输出：diff 节点负度中心性取值情况列表（排序后）
    '''
    negative_degree=Gn.degree()
    sort_negative_degree=list(sorted(negative_degree, key= lambda negative_degree: negative_degree[0]))
    

    n_degree=[]  # 负度值容器
    
   
    for item in sort_negative_degree:
        n_degree.append(item[1])
       
    ndc_value=[]

    for item in n_degree:
	    d=1-float(item)/(len(n_degree)-1)
	    ndc_value.append(d)

    ndc_node=[]  # 对应节点容器
    for i in sort_negative_degree:
	    ndc_node.append(i[0])

    negative_dc=dict(zip(ndc_node, ndc_value))
     
    return negative_dc



# 计算原始网络
G=nx.read_edgelist('N46edge.txt', nodetype=int, data=(('weight', float), ))
# 分离网络
Gn, Gp=separate_network(G)
# 计算节点及其对应的FMF值
negative_dc=negative_degree_centrality(Gn)












