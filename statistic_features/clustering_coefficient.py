# -*- coding: utf-8 -*-
"""
聚类系数
"""


import numpy as np
import pandas as pd 
import networkx as nx

    
def data_trans(file):
    '''将代表负边的权重由2变为-1
    输入：原始txt文件
    输出：权值变化后的t.txt文件
    '''
   
    txt = np.loadtxt(file)  
    data = pd.DataFrame(txt)   # 将txt文件变为DataFrame格式
    data.columns = ['n1', 'n2', 'sign']  # 命名列变量
    
    # 将代表负边的权重由2变为-1
    for i in range(len(data)):
        if data['sign'][i] == 2:
            data['sign'][i] = -1
    data.to_csv('t.txt', index = False, sep = '\t', header = None) 
    return 't.txt'


def c_s(G):
    A = nx.to_numpy_matrix(G)  # 原始网络的带符号矩阵
    B = np.dot(A, A)  # 带符号矩阵的平方
    C = np.multiply(A, B)  # 带符号邻接矩阵H乘带符号矩阵的平方
    part_tri = C.sum()

    A1 = abs(A)  # 将带符号的邻接矩阵取绝对值，变为不带符号的邻接矩阵
    B1 = np.dot(A1, A1)  # 不带符号邻接矩阵的平方
    B1_half = np.triu(B1, 1)  # 取B1矩阵的上半三角形
    full_tri = B1_half.sum()*2

    C = part_tri/full_tri  # 全部节点的平均聚类系数
   
    return C


# 生成权值变换后的t.txt文件
data=data_trans('N46edge.txt')


#%%  要等文件生成后才可调用
G = nx.read_edgelist('C://Users//Administrator//Desktop//statistic_features//t.txt',
                     nodetype=float, data=(('weight', float),))
C=c_s(G)
print('average clustering coefficient of the whole network:'+str(C))























