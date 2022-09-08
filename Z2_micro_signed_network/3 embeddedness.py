
# -*- coding: utf-8 -*-
"""
嵌入性
embeddedness
"""

import networkx as nx
import numpy as np

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

    for node_i, node_j, weight_data in G.edges(data = True):  # 分离顶点与权重
        if 'weight' in weight_data:  # 剔除无权重数据
            list_edge.append([node_i, node_j, weight_data['weight']])  # 顶点权重列表
        else:
            pass
    
    for i in list_edge:  # 正负边分类
        if i[2] == 1:
            positive_edge.append(i)
        elif i[2] == 2:
            negative_edge.append(i)
        else:
            pass
    
    # 构建正边网络与负边网络   
    Gp = nx.Graph()
    Gn = nx.Graph()
    Gp.add_weighted_edges_from(positive_edge)
    Gn.add_weighted_edges_from(negative_edge)
    
    return Gn, Gp


def common_neighbor(G, node_ij):
    '''计算共同邻居节点
    输入 G 原始网络
         node_ij 原始网络节点元组
    输出 cn 节点元组的共同邻居节点数量
    '''
    node_i = node_ij[0]
    node_j = node_ij[1]
    neighbor_i = set(G.neighbors(node_i))
    neighbor_j = set(G.neighbors(node_j))
    neighbor_ij = neighbor_i.intersection(neighbor_j)
    cn = len(neighbor_ij)
    return cn


def cn_em(G, Gpn):
    '''分析连边符号与嵌入性强弱的关系
    输入 G 原始网络
         Gp 正边网络
    输出 em 嵌入性数值与该值下正边比例
    '''
    list_cn=[]
    
    for item in G.edges():  # 得到节点元组
        try:
            item_cn=common_neighbor(Gpn, item)  # 计算公共邻居节点
            list_cn.append((item_cn, G[item[0]][item[1]]['weight']))  # （共同邻居，边值权重）
        except:
            pass
    
    sort_list_cn=sorted(list_cn, key= lambda list_cn: list_cn[0])  # 排序 方便for循环

    sort_list_cn.append((sort_list_cn[-1][0]+1, 0))  # 增加数值 避免for循环漏数据
    
    index_cn=0  # 共同邻居导引数据
    positive_en=0  # 正边数量
    sum_en=0  # 总边数量
    proportion_en=0  # 正边占比
    em={}  # 嵌入性数值与该值下正边比例
	
    for item in sort_list_cn:
	    if item[0] == index_cn:  # 计算正边与总边数
		    if item[1] == 1:
			    positive_en=positive_en+1
		    sum_en=sum_en+1
	    elif item[0] >index_cn:  # 计算上述共同邻居数量下的正边比例
		    if sum_en==0:
			    em[index_cn]=np.nan  ####@@@@@@@@@@
		    else:
			    proportion_en=float(positive_en)/sum_en
			    em[index_cn]=proportion_en
		    index_cn=item[0]  # 为下一个共同邻居数量统计做准备
		    positive_en=0
		    sum_en=0
    return em


# 计算原始网络
G=nx.read_edgelist('N46edge.txt', nodetype=int, data=(('weight', float), ))
# 分离网络
Gn, Gp=separate_network(G)
# 计算嵌入性数值与该值下正边比例
em=cn_em(G, Gp)





















