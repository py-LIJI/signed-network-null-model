"""
测试程序
测试批量读取零模型数据
"""

import networkx as nx
import pandas as pd
import time
import os

start = time.time()

# 控制实证符号网络种类
# file_name = '6_BA'
# file_name = '7_BO'
# file_name = '8_WR'
# file_name = '9_ES'
# file_name = '10_SS'
file_name = '11_S20081106'
# file_name = '12_S20090216'
# file_name = '13_S20090221'
# file_name = '14_EM'

# 控制零模型种类
# null_name = '_pnull_'
null_name = '_nnull_'
# null_name = '_pnnull_'
# null_name = '_full_'
# null_name = '_snull_'

base_dir = os.path.dirname(__file__)  # 当前文件夹目录
# path_read = base_dir + '/data_null_model/' + file_name + null_name + str(i) + '.txt'  # 读取路径
G_null = []

for i in range(50):
    path_read = base_dir + '/data_null_model/' + file_name + null_name + str(i) + '.txt'
    null = nx.read_edgelist(path_read, nodetype=int, data=(('weight', float),))
    G_null.append(null)

end = time.time()
print('用时：', round(end-start, 0), '秒')






