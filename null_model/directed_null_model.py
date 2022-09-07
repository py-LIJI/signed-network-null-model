"""
包含5种有向符号网络零模型：
    正边随机置乱零模型
    负边随机置乱零模型
    正负边分别随机置乱零模型
    完全随机置乱零模型
    符号随机置乱零模型
全局声明：
    +: weight 1
    -: weight 2
有向网络邻居节点：
    3 —> 7: 7是3的邻居节点，3不是7的邻居节点
"""

import networkx as nx
import random
import copy


def directed_positive_swap(G0, nswap=1, max_tries=100):
    """
    :description: 正边随机置乱零模型
    :param G0: 原网络
    :param nswap: 成功置乱次数
    :param max_tries: 最大尝试次数
    :return: 完成乱后的零模型网络
    """
    G = copy.deepcopy(G0)  # 深层次拷贝原网络
    n = 0  # 尝试次数
    swapcount = 0  # 成功完成置乱次数
    a = dict(G.degree())
    keys, degrees = zip(*a.items())  # 获取节点及对应度值
    cdf = nx.utils.cumulative_distribution(degrees)  # 计算度的累积分布，为在网络中随机选取节点做准备

    while swapcount < nswap:
        # 随机选取两个节点
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # 两个节点不能相同
        u = keys[ui]
        x = keys[xi]

        # 为两个节点分别选取邻居节点
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:  # 两个邻居节点不能相同
                continue
        else:
            continue

        # 对原网络进行断边交换重连
        if ((v not in G[x]) and (y not in G[u]) and G[u][v]['weight'] == 1
           and G[x][y]['weight'] == 1):
            if ((x in G[v]) and (G[v][x]['weight'] == 1)) or ((u in G[y]) and (G[y][u]['weight'] == 1)):
                continue
            else:
                G.add_edge(u, y, weight=1)
                G.add_edge(x, v, weight=1)
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1  # 成功置乱次数+1

        n += 1  # 最大尝试次数+1

        # 报错处理
        if n >= max_tries:
            e = ('Maximum number (%s) exceeded, ' % n
                 + 'but successful swaps (%s).' % swapcount)
            print(nx.NetworkXAlgorithmError(e))
            G = 0  # 标记此时的零模型不能使用
            break  # 结束循环

    # 输出完成时成功置乱次数与尝试次数
    print('swap times=', swapcount, 'try times=', n)
    return G


def directed_negative_swap(G0, nswap=1, max_tries=100):
    """
    :description: 负边随机置乱零模型
    :param G0: 原网络
    :param nswap: 成功置乱次数
    :param max_tries: 最大尝试次数
    :return: 完成乱后的零模型网络
    """
    G = copy.deepcopy(G0)  # 深层次拷贝原网络
    n = 0  # 尝试次数
    swapcount = 0  # 成功完成置乱次数
    a = dict(G.degree())
    keys, degrees = zip(*a.items())  # 获取节点及对应度值
    cdf = nx.utils.cumulative_distribution(degrees)  # 计算度的累积分布，为在网络中随机选取节点做准备

    while swapcount < nswap:
        # 随机选取两个节点
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # 两个节点不能相同
        u = keys[ui]
        x = keys[xi]

        # 为两个节点分别选取邻居节点
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:  # 两个邻居节点不能相同
                continue
        else:
            continue

        # 进行断边交换重连
        if ((v not in G[x]) and (y not in G[u]) and G[u][v]['weight'] == 2
           and G[x][y]['weight'] == 2):
            if (((x in G[v]) and (G[v][x]['weight'] == 2)) or
               ((u in G[y]) and (G[y][u]['weight'] == 2))):
                continue
            else:
                G.add_edge(u, y, weight=1)
                G.add_edge(x, v, weight=1)
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1  # 成功置乱次数+1

        n += 1  # 最大尝试次数+1

        # 报错处理
        if n >= max_tries:
            e = ('Maximum number (%s) exceeded, ' % n
                 + 'but successful swaps (%s).' % swapcount)
            print(nx.NetworkXAlgorithmError(e))
            G = 0  # 标记此时的零模型不能使用
            break  # 结束循环

    # 输出完成时成功置乱次数与尝试次数
    print('swap times=', swapcount, 'try times=', n)  # 输出完成时的尝试次数
    return G


def directed_positive_negative_swap(G0, nswap=1, max_tries=100):
    """
    :description: 正负边分别随机置乱零模型
    :param G0: 原网络
    :param nswap: 成功置乱次数
    :param max_tries: 最大尝试次数
    :return: 完成乱后的零模型网络
    """
    G_p = directed_positive_swap(G0, nswap, max_tries)
    G = directed_negative_swap(G_p, nswap, max_tries)
    return G


def directed_full_swap(G0, nswap=1, max_tries=100):
    """
    :description: 完全随机置乱零模型
    :param G0: 原网络
    :param nswap: 成功置乱次数
    :param max_tries: 最大尝试次数
    :return: 完成乱后的零模型网络
    """
    G = copy.deepcopy(G0)  # 深层次拷贝原网络
    n = 0  # 尝试次数
    swapcount = 0  # 成功完成置乱次数
    a = dict(G.degree())
    keys, degrees = zip(*a.items())  # 获取节点及对应度值
    cdf = nx.utils.cumulative_distribution(degrees)  # 计算度的累积分布，为在网络中随机选取节点做准备

    while swapcount < nswap:
        # 随机选取两个节点
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # 两个节点不能相同
        u = keys[ui]
        x = keys[xi]

        # 为两个节点分别选取邻居节点
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:  # 两个邻居节点不能相同
                continue
        else:
            continue

        # 进行断边交换重连
        if (v not in G[x]) and (y not in G[u]):
            if (x in G[v]) or (u in G[y]):
                continue
            else:
                G.add_edge(u, y, weight=G[u][v]['weight'])
                G.add_edge(x, v, weight=G[x][y]['weight'])
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1

        n += 1  # 最大尝试次数+1

        # 报错处理
        if n >= max_tries:
            e = ('Maximum number (%s) exceeded, ' % n
                 + 'but successful swaps (%s).' % swapcount)
            print(nx.NetworkXAlgorithmError(e))
            G = 0  # 标记此时的零模型不能使用
            break  # 结束循环

    # 输出完成时成功置乱次数与尝试次数
    print('swap times=', swapcount, 'try times=', n)  # 输出完成时的尝试次数
    return G


def directed_sign_swap(G0, nswap=1, max_tries=100):
    """
    :description: 符号随机置乱零模型
    :param G0: 原网络
    :param nswap: 成功置乱次数
    :param max_tries: 最大尝试次数
    :return: 完成乱后的零模型网络
    """
    G = copy.deepcopy(G0)  # 深层次拷贝原网络
    n = 0  # 尝试次数
    swapcount = 0  # 成功完成置乱次数
    a = dict(G.degree())
    keys, degrees = zip(*a.items())  # 获取节点及对应度值
    cdf = nx.utils.cumulative_distribution(degrees)  # 计算度的累积分布，为在网络中随机选取节点做准备

    while swapcount < nswap:
        # 随机选取两个节点
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # 两个节点不能相同
        u = keys[ui]
        x = keys[xi]

        # 为两个节点分别选取邻居节点
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:  # 两个邻居节点不能相同
                continue
        else:
            continue

        # 进行符号交换
        if (G.is_directed() and u in G[v]) or (G.is_directed() and x in G[y]):
            continue
        else:
            G[u][v]['weight'], G[x][y]['weight'] = G[x][y]['weight'], G[u][v]['weight']
            if G[u][v]['weight'] != G[x][y]['weight']:
                swapcount += 1

        n += 1  # 最大尝试次数+1

        # 报错处理
        if n >= max_tries:
            e = ('Maximum number (%s) exceeded, ' % n
                 + 'but successful swaps (%s).' % swapcount)
            print(nx.NetworkXAlgorithmError(e))
            G = 0  # 标记此时的零模型不能使用
            break  # 结束循环

    # 输出完成时成功置乱次数与尝试次数
    print('swap times=', swapcount, 'try times=', n)  # 输出完成时的尝试次数
    return G


if __name__ == '__main__':
    G0 = nx.read_edgelist(r'..\signed_network_data\N46edge.txt', create_using=nx.DiGraph(), nodetype=int, data=(('weight', float), ))
    print('原网络：', G0)

    positive = directed_positive_swap(G0, 400, 2000)
    negative = directed_negative_swap(G0, 10, 2000)
    pos_neg = directed_positive_negative_swap(G0, 10, 2000)
    full = directed_full_swap(G0, 400, 2000)
    sign = directed_sign_swap(G0, 400, 2000)

    print('正边置乱零模型', positive)
    print('负边置乱零模型', negative)
    print('正负边分别置乱零模型', pos_neg)
    print('完全置乱零模型', full)
    print('符号置乱零模型', sign)

