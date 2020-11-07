# -*- coding: utf-8 -*-
"""
匹配系数（无向符号网络）
"""


import numpy as np
import networkx as nx
import copy


def divide_degree(G):
    '''首先将原始网络G拆分成正边网络和负边网络
    输入：G原始网络
    输出：p正边数据列表
         n负边数据列表
         Gp正边网络
         Gn负边网络
    '''
    
    edges = G.edges(data = True)
    pos_edges = []  # 正边数据容器
    neg_edges = []  # 负边数据容器

    posdegree_graph = copy.deepcopy(G)  # 拥有正度值网络
    negdegree_graph = copy.deepcopy(G)  # 拥有负度值网络

    for item in edges:
        if item[2]['weight'] == 1:
            pos_edges.append(item)
            negdegree_graph.remove_edge(item[0], item[1])
        if item[2]['weight'] == 2:
            neg_edges.append(item)
            posdegree_graph.remove_edge(item[0], item[1])
                
    return posdegree_graph, negdegree_graph, pos_edges, neg_edges


def sum_jk(Gpdeg, Gndeg, pos_edges, neg_edges):
    '''计算无向符号网络的4种度相关性（公式模块）
         +-- 网络中正连接的两个节点正正度匹配特性
         ++- 网络中正连接的两个节点正负度匹配特性
         -++ 网络中负连接的两个节点正正度匹配特性
         -+- 网络中负连接的两个节点正负度匹配特性
    输入：pos_edges正边数据列表
         neg_edges负边数据列表
         Gpdeg正边网络
         Gndeg负边网络
    输出：jn_kn, jn_kn1, jn_kn2, +--公式模块
         jp_kn, jp_kn1, jp_kn2, ++-公式模块
         jp_kp, jp_kp1, jp_kp2, -++公式模块
         jp_kn3, jp_kn4, jp_kn5，-+-公式模块
    '''
        
    # +--
    jnkn = []
    jnkn1 = []
    jnkn2 = []

    # ++-
    jpkn = []
    jpkn1 = []
    jpkn2 = []

    # -++
    jpkp = []
    jpkp1 = []
    jpkp2 = []

    # -+-
    jpkn3 = [] 
    jpkn4 = []
    jpkn5 = []

    for edge1 in pos_edges:
        
        # +--
        a = int(Gndeg.degree(edge1[0])) * int(Gndeg.degree(edge1[1]))
        jnkn.append(a)
        jn_kn = sum(jnkn)
    
        b = int(Gndeg.degree(edge1[0])) + int(Gndeg.degree(edge1[1]))
        b1 = 0.5*b
        jnkn1.append(b1)
        jn_kn1 = sum(jnkn1)
        
        c = (np.square(int(Gndeg.degree(edge1[0])))
             + np.square(int(Gndeg.degree(edge1[1]))))
        c1 = 0.5*c
        jnkn2.append(c1)
        jn_kn2 = sum(jnkn2)
        
        # ++-        
        o = int(Gpdeg.degree(edge1[0])) * int(Gndeg.degree(edge1[1]))
        jpkn.append(o)
        jp_kn = sum(jpkn)
        
        p = int(Gpdeg.degree(edge1[0])) + int(Gndeg.degree(edge1[1]))
        p1 =  0.5*p
        jpkn1.append(p1)
        jp_kn1 = sum(jpkn1)
        
        q = (np.square(int(Gpdeg.degree(edge1[0]))) 
             + np.square(int(Gndeg.degree(edge1[1]))))
        q1 = 0.5*q
        jpkn2.append(q1)
        jp_kn2 = sum(jpkn2)
        
    for edge2 in neg_edges:
       
        # -++
        d = int(Gpdeg.degree(edge2[0]))*int(Gpdeg.degree(edge2[1]))
        jpkp.append(d)
        jp_kp = sum(jpkp)
        
        e = int(Gpdeg.degree(edge2[0])) + int(Gpdeg.degree(edge2[1]))
        e1 = 0.5*e
        jpkp1.append(e1)
        jp_kp1 = sum(jpkp1)
        
        f = (np.square(int(Gpdeg.degree(edge2[0]))) 
             + np.square(int(Gpdeg.degree(edge2[1]))))
        f1 = 0.5*f
        jpkp2.append(f1)
        jp_kp2 = sum(jpkp2)
        
        # -+-
        r = int(Gpdeg.degree(edge2[0])) * int(Gndeg.degree(edge2[1]))
        jpkn3.append(r)
        jp_kn3=sum(jpkn3)
        
        s = int(Gpdeg.degree(edge2[0])) + int(Gndeg.degree(edge2[1]))
        s1 = 0.5*s
        jpkn4.append(s1)
        jp_kn4 = sum(jpkn4)
        
        t = (np.square(int(Gpdeg.degree(edge2[0]))) 
             + np.square(int(Gndeg.degree(edge2[1]))))
        t1 = 0.5*t
        jpkn5.append(t1)
        jp_kn5 = sum(jpkn5)
    
    return (jn_kn, jn_kn1, jn_kn2, jp_kn, jp_kn1, jp_kn2, 
            jp_kp, jp_kp1, jp_kp2, jp_kn3, jp_kn4, jp_kn5)



def final_formula(a, q, w, e):  
    '''匹配系数计算公式
    输入：a为正边或负边数量
         q,w,e分别为三组公式模块
    输出：formula匹配系数公式（Newman）
    '''
              
    formula = (1/a * q - (1/a*w)*(1/a*w))/(1/a * e - (1/a*w)*(1/a*w))

    return formula


# 代入数值生成网络
G = nx.read_edgelist('C://Users//Administrator//Desktop//statistic_features//N46edge.txt', 
                     nodetype=int, data=(('weight', float),))
# 计算各种公式模块数值
Gpdeg, Gndeg, pos_edges, neg_edges = divide_degree(G)
a0, b0, c0, d0, e0, f0, g0, h0, i0, j0, k0, l0 = sum_jk(Gpdeg, Gndeg, 
                                                        pos_edges, neg_edges)
# 组装成各自匹配特性数值
pnn = final_formula(len(pos_edges), a0, b0, c0)
ppn = final_formula(len(pos_edges), d0, e0, f0)
npp = final_formula(len(neg_edges), g0, h0, i0)
npn = final_formula(len(neg_edges), j0, k0, l0)
# 输出各自匹配特性数值
print("The assortativity coefficient of +-- in the original network is:",
      "%3.3f" %pnn)
print("The assortativity coefficient of ++- in the original network is:",
      "%3.3f" %ppn)
print("The assortativity coefficient of -++ in the original network is:",
      "%3.3f" %npp)
print("The assortativity coefficient of -+- in the original network is:",
      "%3.3f" %npn)



