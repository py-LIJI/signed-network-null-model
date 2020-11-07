# -*- coding: utf-8 -*-
"""该模块是无向符号网络1阶零模型的构造方法之一:
   将原始网络模型，通过正负边分别随机断边重连零模型函数，生成无向符号网络1阶零模型
    
   全局声明：
       + : weight = 1
       - : weight = 2
"""


import matplotlib.pyplot as plt
import networkx as nx
import random
import copy


def sign_network_positive_swap(G0, nswap=1, max_tries=100):    
    """正边随机断边重连零模型函数
    
    输入：
        G0: 原始网络模型
        nswap: 断边交换次数
        max_tries：最大尝试次数
        
    输出：
        G：按要求断边重连1阶零模型
    """
    
    G = copy.deepcopy(G0)  # 深层次拷贝，不会产生任何映射
    n = 0
    swapcount = 0  
    a = dict(G.degree())
    keys, degrees = zip(*a.items())  # 获取keys, degree
    cdf = nx.utils.cumulative_distribution(degrees)  # 由degrees求取cdf
        
    while swapcount < nswap:
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        
        if ui == xi:
            continue  # 来源相同，跳过
       
        u = keys[ui]  # 转换索引标签
        x = keys[xi]
       
        # 从相邻中统一选择目标
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue
        
        #该部分进行断边交换重连
        if ((x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 1 
            and G[x][y]['weight'] == 1):
            G.add_edge(u, x, weight=1)
            G.add_edge(v, y, weight=1)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            swapcount += 1
           
        if n >= max_tries:
            e = ('Maximum number of swap attempts (%s) exceeded '%n
                 +'before desired swaps achieved (%s).'%nswap)
            print(nx.NetworkXAlgorithmError(e))
            break
        
        n += 1
        
        if n%1000000 == 0:
            print('swap times=', swapcount, 'try times=', n)
    
    return G        




def sign_network_negative_swap(G0, nswap=1, max_tries=100):    
    """负边随机断边重连零模型函数
    
    输入：
        G0: 原始网络模型
        nswap: 断边交换次数
        max_tries：最大尝试次数
        
    输出：
        G：按要求断边重连1阶零模型
    """
    
    G = copy.deepcopy(G0)  # 深层次拷贝，不会产生任何映射
    n = 0
    swapcount = 0
    b = dict(G.degree())
    keys, degrees = zip(*b.items())  # 获取keys, degree
    cdf = nx.utils.cumulative_distribution(degrees)  # 由degrees得到cdf
        
    while swapcount < nswap:
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        
        if ui == xi:
            continue  # 来源相同，跳过
        
        u = keys[ui]  # 转换索引标签
        x = keys[xi]
        
        # 从相邻中统一选择目标
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue
        
        #该部分进行断边交换重连
        if ((x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 2 
            and G[x][y]['weight'] == 2):
            G.add_edge(u, x, weight=2)
            G.add_edge(v, y, weight=2)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            swapcount += 1
            
        if n >= max_tries:
            e = ('Maximum number of swap attempts (%s) exceeded '%n 
                 + 'before desired swaps achieved (%s).'%nswap)
            print(nx.NetworkXAlgorithmError(e))
            break
        
        n += 1
        
        if n%1000000 == 0:
            print ('swap times=', swapcount, 'try times=', n)
    
    return G


#%%  计算网络

# 计算原始网络模型（G0）
G0 = nx.read_edgelist('filename.txt', nodetype=int, data=(('weight',float),))       
# 计算基于正负边分别随机断边重连的无向符号网络1阶零模型（G3）
G1 = sign_network_positive_swap(G0, 60000, 100000)  
G3 = sign_network_negative_swap(G1, 60000, 100000)    


#%% 可视化

# G0可视化
# 按权重划分为正边和负边
p_edge = [(u, v) for (u, v, d) in G0.edges(data = True) if d['weight'] <= 1]
n_edge = [(u, v) for (u, v, d) in G0.edges(data = True) if d['weight'] > 1]
# 首先画出节点
pos = nx.spring_layout(G0)
nx.draw_networkx_nodes(G0, pos)
# 再分别画出正边和负边
nx.draw_networkx_edges(G0, pos, edgelist = p_edge)
nx.draw_networkx_edges(G0, pos, edgelist = n_edge, style = 'dashed')
plt.show()


# G3可视化
# 按权重划分为正边和负边
p_edge = [(u, v) for (u, v, d) in G3.edges(data = True) if d['weight'] <= 1]
n_edge = [(u, v) for (u, v, d) in G3.edges(data = True) if d['weight'] > 1]
# 首先画出节点
pos = nx.spring_layout(G3)
nx.draw_networkx_nodes(G3, pos)
# 再分别画出正边和负边
nx.draw_networkx_edges(G3, pos, edgelist = p_edge)
nx.draw_networkx_edges(G3, pos, edgelist = n_edge, style = 'dashed')
plt.show()





