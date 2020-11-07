# -*- coding: utf-8 -*-
"""该模块是无向符号网络1阶零模型的构造方法之一:
   将原始网络模型，通过正边随机断边重连零模型函数，生成无向符号网络1阶零模型
    
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
    a = dict(G.degree())  # 形成所有节点-度字典
    keys, degrees = zip(*a.items()) 
    '''获取节点keys, 度degrees
    其中的a.items()以列表的形式返回可遍历的键-值对元组
    zip本身为打包成元组的函数，加*是解包元组，返回键值对
    '''
    
    cdf = nx.utils.cumulative_distribution(degrees)  
    '''计算度degrees的累积分布cdf(概率)
    所谓的累积分布函数与概率所讲分布函数同义
    '''    
    
    while swapcount < nswap:
        # 返回度值为2的节点索引 
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)  # 离散序列函数
         
        
        if ui == xi:
            continue  # 来源相同，跳过，所招节点索引不能指向同一个节点
       
        u = keys[ui]  # 根据索引找到节点 
        x = keys[xi]
       
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            '''从相邻中统一选择目标
            从节点u,x出发，找到直接相邻的节点对x,y  u,v
            '''
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue
        
        #该部分进行断边交换重连
        if ((x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 1 
            and G[x][y]['weight'] == 1):
            '''操作条件：如果 节点变量x与u不重合 and 节点变量y与v不重合 
            and u,v间为正边 and x,y间为正边。则：在节点变量u,x间添加边，边的属性为正;
            在节点变量u,x间添加边，边的属性为正;去除原u,v间的边;去除原x,y间的边;
            断边交换次数自增1
            '''
            G.add_edge(u, x, weight=1)  
            G.add_edge(v, y, weight=1)  
            G.remove_edge(u, v)  
            G.remove_edge(x, y)  
            swapcount += 1
           
        if n >= max_tries:  # 报错处理
            # 在所需的交换达到nswap之前，已超过最大交换尝试次数n
            e = ('Maximum number of swap attempts (%s) exceeded '%n
                 +'before desired swaps achieved (%s).'%nswap)            
            print(nx.NetworkXAlgorithmError(e))
            break
        
        n += 1
        
        if n%1000000 == 0:
            print('swap times=', swapcount, 'try times=', n)
    
    return G  


#%%  计算网络
# 计算原始网络模型(G0)
G0 = nx.read_edgelist('C://Users//Administrator//Desktop//sign_null_model_undirected//N46edge.txt', nodetype=int, data=(('weight', float),))      
# 计算基于正边随机断边重连的无向符号网络1阶零模型(G1)
G1 = sign_network_positive_swap(G0, 60000, 100000)  

 
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


# G1可视化
# 按权重划分为正边和负边
p_edge = [(u, v) for (u, v, d) in G1.edges(data = True) if d['weight'] <= 1]
n_edge = [(u, v) for (u, v, d) in G1.edges(data = True) if d['weight'] > 1]
# 首先画出节点
pos = nx.spring_layout(G1)
nx.draw_networkx_nodes(G1, pos)
# 再分别画出正边和负边
nx.draw_networkx_edges(G1, pos, edgelist = p_edge)
nx.draw_networkx_edges(G1, pos, edgelist = n_edge, style = 'dashed')
plt.show()












