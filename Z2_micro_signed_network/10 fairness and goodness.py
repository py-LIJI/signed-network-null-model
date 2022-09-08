# -*- coding: utf-8 -*-
"""
fairness and goodness 
"""

import networkx as nx


def goodness(old_F, t, node_i, G, dict_edge):
    '''计算优秀度值
    输入 old_F 上一次迭代的公平度指标值
         t 为第一次递归代入初值
         node_i 需要计算优秀度值的节点
         G 原始网络
         dict_edge {（节点，节点）：边权重}
    输出 g 节点node_i的优秀度值
    '''
    inv=list(G.neighbors(node_i))  # 得到node_i的邻居节点列表
    Lj=0  # 公式累加部分
    
    for item in inv:
        try:  # 找到权重
            w=dict_edge[(node_i, item)]
        except:
            w=dict_edge[(item, node_i)]
        if t==0:  # 代入递归初值
            f=1
        else:
            f=old_F
        Lj=Lj+f*w  # 计算累加部分
    
    g=float(Lj)/len(inv)  # 计算优秀度值
    
    return g


def fairness(new_G, node_i, G, dict_edge):
    '''计算公平度值
    输入 new_G 迭代后新的优秀度值
         node_i 需要计算优秀度值的节点
         G 原始网络
         dict_edge {（节点，节点）：边权重}
    输出 f 节点node_i的公平度值
    '''
    out=list(G.neighbors(node_i))  # 得到node_i的邻居节点列表
    Lj=0 # 公式累加部分
    
    for item in out:
        try:  # 找到权重
            w=dict_edge[(node_i, item)]
        except:
            w=dict_edge[(item, node_i)]
        Lj=Lj+abs(w-new_G)  # 计算累加部分
    
    f=1-float(Lj)/(2*len(out))  # 计算公平度值
    
    return f   
  

def fairness_goodness(G):
    dict_edge={}  # {（节点，节点）：边权重}
    for u, v, weight_data in G.edges(data=True):
        if 'weight' in weight_data:
            dict_edge[(u, v)]=weight_data['weight']
        else:
            pass
    
    list_node=list(G.nodes())  # 得到节点列表
    old_G=1  # 优秀度递归初值
    old_F=1  # 公平度递归初值
    dict_nfg={}  # {节点：(公平度值， 优秀度值)}
    
    for node_i in list_node:  # 每个节点依次计算
        for t in range(10000):  # 方便代入初值计算及循环
            new_G=goodness(old_F, t, node_i, G, dict_edge)
            new_F=fairness(new_G, node_i, G, dict_edge)
            if abs(new_F-old_F)>0.001 or abs(new_G-old_G)>0.001:  # 判断循环是否结束
                break
            else:  # 递归迭代
                old_F=new_F
                old_G=new_G
        dict_nfg[node_i]=(new_F, new_G)
      
    return dict_nfg


# 得到原始网络
G = nx.read_edgelist('N46edge.txt', nodetype=int, data=(('weight', float),))
# 计算结果{节点：(公平度值， 优秀度值)}
dict_nfg=fairness_goodness(G)
























