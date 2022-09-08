"""
符号网络数据预处理：
将负边改由-1表示
"""

import pandas as pd
import numpy as np
import os
import time
import networkx as nx
import undirected_null_model as null_model


# def trans_weight(file):
#     """将正边变为1，负边变为-1，格式依然为三元组"""
#
#     base_dir = os.path.dirname(__file__) # 获取当前文件目录路径
#     path_1 = os.path.join(base_dir, 'data_original', file) # 合并为数据获取路径
#
#     data = pd.read_table(path_1, sep='\s+', header=None,
#                          names=['n1', 'n2', 'sign'])  # '\s+'读取多空格或teb键分隔数据
#     data = data.replace({'sign': 2}, -1) # 负边换为-1
#
#     path_2 = os.path.join(base_dir, 'data_median', file)  # 合并为数据保存路径
#     data.to_csv(path_2, sep='\t', index=False, header=None)  # 保存数据
#
#     return file


def trans_null(file_name, exp_n):
    """
    证网络生成零模型后存储
    输入文件名，期望生成零模型的个数，成功生成零模型的个数
    """
    base_dir = os.path.dirname(__file__)  # 当前目录文件夹
    path_read = base_dir + '/data_median/' + file_name + '.txt'  # 读取路径
    G0 = nx.read_edgelist(path_read, nodetype=int, data=(('weight', float), ))
    suc_n = 0  # 成功生成零模型个数

    number_p = 0  # 负边总数统计
    for i,j,weight in G0.edges(data=True):
        if weight['weight'] < 0:
            number_p += 1

    # 负边置乱、正负边分别置乱时exp_swap = number_p, max_swap = 20 * len(G0.edges())
    # 正边置乱、完全置乱时exp_swap = len(G0.edges()), max_swap = 5 * exp_swap
    exp_swap_p = len(G0.edges())  # 零模型期望达到的置乱次数
    max_swap_p = 10 * len(G0.edges())  # 零模型最大尝试次数
    exp_swap_n = number_p  # 零模型期望达到的置乱次数
    max_swap_n = 20 * len(G0.edges())  # 零模型最大尝试次数

    G_null=[]
    for i in range(exp_n):
        # null_p = null_model.sign_network_positive_swap(G0, exp_swap_p, max_swap_p)
        # null_n = null_model.sign_network_negative_swap(null_p, exp_swap_n, max_swap_n)
        # null = null_model.sign_network_full_swap(null_n, 3 * exp_swap_p, max_swap_p)
        null = null_model.sign_network_sign_swap(G0, exp_swap_p, max_swap_n)
        if null != 0:
            suc_n += 1
            G_null.append(null)

    for i in range(suc_n):
        # path_write = base_dir + '/data_null_model/' + file_name + '_pnull_' + str(i) +'.txt'
        # path_write = base_dir + '/data_null_model/' + file_name + '_nnull_' + str(i) + '.txt'
        # path_write = base_dir + '/data_null_model/' + file_name + '_pnnull_' + str(i) + '.txt'
        # path_write = base_dir + '/data_null_model/' + file_name + '_fnull_' + str(i) + '.txt'
        path_write = base_dir + '/data_null_model/' + file_name + '_snull_' + str(i) + '.txt'
        nx.write_weighted_edgelist(G_null[i], path_write, delimiter='\t', encoding='utf-8')

    return suc_n


if __name__ == '__main__':
    start = time.time()
    # suc_n = trans_null('6_BA', exp_n=50)
    suc_n = trans_null('7_BO', exp_n=50)
    suc_n = trans_null('8_WR', exp_n=50)
    suc_n = trans_null('9_ES', exp_n=50)
    suc_n = trans_null('10_SS', exp_n=50)
    suc_n = trans_null('11_S20081106', exp_n=50)
    suc_n = trans_null('12_S20090216', exp_n=50)
    suc_n = trans_null('13_S20090221', exp_n=50)
    suc_n = trans_null('14_EM', exp_n=50)
    end = time.time()
    print('总共用时：', round(end-start, 0), '秒','\n')
    # print('生成零模型的个数：', suc_n)



