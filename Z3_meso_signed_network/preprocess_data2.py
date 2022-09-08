"""
将符号网络变为无符号网络
将数据保存在data/no_signed中
"""

import networkx as nx
import pandas as pd
import time
import os

start = time.time()

# 控制实证符号网络种类
# file_name = '2_RD'
# file_name = '3_RHT'
# file_name = '4_SM'
file_name = '5_FT'

# file_name = '9_ES'
# file_name = '10_SS'
# file_name = '11_S20081106'
# file_name = '12_S20090216'
# file_name = '13_S20090221'
# file_name = '14_EM'

# 控制零模型种类
# null_name = '_pnull_'
# null_name = '_nnull_'
# null_name = '_pnnull_'
# null_name = '_fnull_'
null_name = '_snull_'

base_dir = os.path.dirname(__file__)  # 当前文件夹目录
# path_read = base_dir + '/data_null_model/' + file_name + null_name + str(i) + '.txt'  # 读取路径

# 原网络处理
# path_read = base_dir + '/data/signed/' + file_name + '.txt'
# G0 = nx.read_edgelist(path_read, nodetype=int, data=(('weight', float),))
# path_write = base_dir + '/data/no_signed/' + file_name + '.txt'
# nx.write_edgelist(G0, path_write, data=False)


# 零模型处理
G_null = []
for i in range(50):
    path_read = base_dir + '/data/signed/' + file_name + null_name + str(i) + '.txt'
    null = nx.read_edgelist(path_read, nodetype=int, data=(('weight', int),))
    path_write = base_dir + '/data/no_signed/' + file_name + null_name + str(i) + '.txt'
    nx.write_edgelist(null, path_write, data=False)


end = time.time()
print('用时：', round(end-start, 0), '秒')






