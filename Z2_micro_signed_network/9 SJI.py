# -*- coding: utf-8 -*-
"""
Signed Jaccard Index
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


def neighbor(Gp, Gn, node_ij):
	node_i=node_ij[0]
	node_j=node_ij[1]
	p_i=set(Gp.neighbors(node_i))
	p_j=set(Gp.neighbors(node_j))
	n_i=set(Gn.neighbors(node_i))
	n_j=set(Gn.neighbors(node_j))
	p_inter=len(p_i & p_j)
	n_inter=len(n_i & n_j)
	pn_inter=len(n_i & p_j)
	pn_union=len(p_i | n_i | p_j | n_j)
	return  p_inter, n_inter, pn_inter, pn_union


def s_j_i(G, Gp, Gn):
	list_r=[]
	for node_ij in G.edges():  # 得到节点元组
	    try:
		    p_inter, n_inter, pn_inter, pn_union=neighbor(Gp, Gn, node_ij)  # 计算公共邻居节点
		    r_ij=float(p_inter+n_inter-p_inter-pn_inter)/pn_union   # （共同邻居，边值权重）
		    list_r.append([node_ij[0], node_ij[1], r_ij])
	    except:
		    pass

	return list_r


# 计算原始网络
G=nx.read_edgelist('N46edge.txt', nodetype=int, data=(('weight', float), ))
# 分离网络
Gn, Gp=separate_network(G)
# 计算嵌入性数值与该值下正边比例
sji=s_j_i(G, Gp, Gn)


#%% 排序

list_sign=[]

for item in sji:
    
    sji_i=item[0]
    sji_j=item[1]
    
    sign=0
    
    for edge_i, edge_j, weight_data in G.edges(data=True):
        if sji_i==edge_i and sji_j==edge_j:
            sign=weight_data['weight']
            
        elif sji_i==edge_j and sji_j==edge_i:
            sign=weight_data['weight']
        
        else:
            pass
    
    list_sign.append([item[2], sign])


























