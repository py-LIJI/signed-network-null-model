# -*- coding: utf-8 -*-
"""
集聚系数
clustering coefficient
"""

import numpy as np
import pandas as pd 
import networkx as nx


def replace_data(file):
    '''将负边的权重由2变为-1
    输入 'N46edge.txt'
    输出 't.txt'
    '''
    data=pd.read_table(file, sep='\s+', header=None, names=['n1', 'n2', 'sign'])  # '\s+'读取多空格或teb键分隔数据
    data=data.replace({'sign': 2}, -1)  # 将'sign'列中的2替换为-1
    data.to_csv('t.txt', sep='\t', index=False, header=None)
    return 't.txt'

def func_c(G):
    '''计算网络的集聚系数
    输入 G 原始网络
    输出 c_c 网络聚类系数
    '''
    A = nx.to_numpy_matrix(G)  # 原始网络的带符号矩阵
    B = np.dot(A, A)  # 带符号矩阵的平方
    C = np.multiply(A, B)  # 带符号邻接矩阵H乘带符号矩阵的平方
    part_tri = C.sum()

    A1 = abs(A)  # 将带符号的邻接矩阵取绝对值，变为不带符号的邻接矩阵
    B1 = np.dot(A1, A1)  # 不带符号邻接矩阵的平方
    B1_half = np.triu(B1, 1)  # 取B1矩阵的上半三角形
    full_tri = B1_half.sum()*2
    
    c_c = part_tri/full_tri  # 全部节点的平均聚类系数
    return c_c

# 首先运行产生替换后的文件t.txt
# replace_data('N46edge.txt')

# 产生原始网络G
G = nx.read_edgelist('t.txt', nodetype=float, data=(('weight', float),))

# 计算集聚系数
c_c = func_c(G)


